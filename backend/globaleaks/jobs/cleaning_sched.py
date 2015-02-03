# -*- coding: UTF-8
#
#   cleaning_sched
#   **************
#
# Implementation of the cleaning operations (delete incomplete submission,
# delete expired tips, etc)

import os
import sys

from twisted.internet.defer import inlineCallbacks

from globaleaks.settings import transact, transact_ro, GLSetting
from globaleaks.utils.utility import log, is_expired, datetime_to_ISO8601, ISO8601_to_datetime
from globaleaks.jobs.base import GLJob
from globaleaks.models import InternalTip, ReceiverFile, InternalFile, Comment

__all__ = ['CleaningSchedule']

@transact_ro
def get_tiptime_by_marker(store, marker):
    itip_list = store.find(InternalTip, InternalTip.mark == marker)

    tipinfo_list = []
    for itip in itip_list:

        comment_cnt = store.find(Comment, Comment.internaltip_id == itip.id).count()
        files_cnt = store.find(InternalFile, InternalFile.internaltip_id == itip.id).count()

        if not itip.context:
            log.err("A Tip related to a not existent Context! This would not happen if delete on cascade is working")
            # And the removal is forced putting 1 second of life to the Tip.
            tip_timetolive = 1
            submission_timetolive = 1
        else:
            tip_timetolive = itip.context.tip_timetolive
            submission_timetolive = itip.context.submission_timetolive

        serialized_tipinfo = {
            'id': itip.id,
            'creation_date': datetime_to_ISO8601(itip.creation_date),
            'expiration_date': datetime_to_ISO8601(itip.expiration_date),
            'tip_life_seconds':  tip_timetolive,
            'submission_life_seconds':  submission_timetolive,
            'files': files_cnt,
            'comments': comment_cnt,
        }
        tipinfo_list.append(serialized_tipinfo)

    return tipinfo_list


@transact
def itip_cleaning(store, tip_id):
    """
    @param tip_id: aim for an InternalTip, and delete them.
    """
    tit = store.find(InternalTip, InternalTip.id == tip_id).one()

    if not tit: # gtfo
        log.err("Requested invalid InternalTip id in itip_cleaning! %s" % tip_id)
        return

    comments = store.find(Comment, Comment.internaltip_id == tip_id)
    log.debug("[-] Removing [%d comments] [%d files] [%d rtips] from an InternalTip" %
        (comments.count(), tit.internalfiles.count(), tit.receivertips.count() ))

    for ifile in tit.internalfiles:
        abspath = os.path.join(GLSetting.submission_path, ifile.file_path)
        ifname = unicode(ifile.name)

        if os.path.isfile(abspath):
            try:
                log.debug("Removing internalfile %s" % abspath)
                os.remove(abspath)
            except OSError as excep:
                log.err("Unable to remove %s: %s" % (abspath, excep.strerror))
        else:
            if ifile.mark != u'delivered': # Removed
                log.err("Unable to remove non existent internalfile %s (itip %s, internalfile %s(%d))" %
                        (abspath, tip_id, ifname, ifile.size))

        rfiles = store.find(ReceiverFile, ReceiverFile.internalfile_id == ifile.id)
        for rfile in rfiles:
            # The following code must be bypassed if rfile.file_path == ifile.filepath
            if rfile.file_path == ifile.file_path:
                continue

            abspath = os.path.join(GLSetting.submission_path, rfile.file_path)

            if os.path.isfile(abspath):
                try:
                    print "Removing receiverfile %s" % abspath
                    os.remove(abspath)
                except OSError as excep:
                    log.err("Unable to remove %s: %s" % (abspath, excep.strerror))
            else:
                if rfile.status == 'encrypted': # encrypted is the only status where the file need to be deleted.
                                                # other cases are:
                                                # - reference: the ifile removal is handled above
                                                # - nokey and unavailable are the error cases where the file does not exist
                    log.err("Unable to remove non existent receiverfile %s (itip %s, internalfile %s(%d))" %
                            (abspath, tip_id, ifname, ifile.size))

    store.remove(tit)


class CleaningSchedule(GLJob):

    @inlineCallbacks
    def operation(self):
        """
        Goal of this function is to check all the submission not
        finalized, and, if the expiration time sets in the context has
        been reached, then clean the submission_id along with the fields,
        and, if present, the uploaded folder/files.

        Second goal of this function, is to check all the InternalTip(s)
        and their expiration date, if match, remove that, all the folder,
        comment and tip related.

        Third goal of this function is to reset the exception counter that
        acts as limit for mail storm
        """
        try:
            # First Goal
            submissions = yield get_tiptime_by_marker(u'submission')
            log.debug("(Cleaning routines) %d unfinished Submission are check if expired" % len(submissions))
            for submission in submissions:
                if is_expired(ISO8601_to_datetime(submission['creation_date']), GLSetting.defaults.submission_seconds_of_life):
                    log.info("Deleting an unfinalized Submission (creation %s expiration %s) files %d" %
                             (submission['creation_date'], submission['expiration_date'], submission['files']) )
                    yield itip_cleaning(submission['id'])

            # Second Goal
            tips = yield get_tiptime_by_marker(u'first')
            log.debug("(Cleaning routines) %d Tips stored are check if expired" % len(tips))
            for tip in tips:
                if is_expired(ISO8601_to_datetime(tip['expiration_date'])):
                    log.info("Deleting an expired Tip (creation date: %s, expiration %s) files %d comments %d" %
                             (tip['creation_date'], tip['expiration_date'], tip['files'], tip['comments']) )
                    yield itip_cleaning(tip['id'])

            # Third Goal: Reset of GLSetting.exceptions
            GLSetting.exceptions = {}

        except Exception as excep:
            log.err("Exception failure in submission/tip cleaning routine (%s)" % excep.message)
            sys.excepthook(*sys.exc_info())
