# -*- coding: utf-8 -*-
#
#   statistics_sched
#   ****************
#
#  Statistics works collecting every N-th minutes the amount of important
#  operations happened
#
#  This impact directly the statistics collection for OpenData purpose and
#  private information.
#  The anomaly detection based on stress level measurement.

import os
from twisted.internet import defer

from globaleaks.anomaly import Alarm
from globaleaks.jobs.base import GLJob
from globaleaks.settings import GLSetting, transact
from globaleaks.models import Stats, Anomalies
from globaleaks.utils.utility import log, datetime_now

@transact
def save_anomalies(store, anomalies_list):

    anomalies_counter = 0
    for anomaly in anomalies_list:
        anomalies_counter += 1
        when_anomaly, anomaly_desc, alarm_raised = anomaly

        newanom = Anomalies()

        newanom.alarm = alarm_raised
        newanom.stored_when = when_anomaly
        newanom.events = anomaly_desc

        store.add(newanom)

    if anomalies_counter:
        log.debug("Saved %d anomalies collected during the last hour" % anomalies_counter)


@transact
def save_statistics(store, start, end, activity_collection):

    newstat = Stats()

    if activity_collection:
        log.debug("since %s to %s I've collected: %s" %
                  (start, end, activity_collection) )

    newstat.start = start
    newstat.summary = dict(activity_collection)
    newstat.freemb = ResourceChecker.get_free_space()

    store.add(newstat)


class AnomaliesSchedule(GLJob):
    """
    This class check for Anomalies, using the Alarm() object
    implemented in anomaly.py
    """

    @defer.inlineCallbacks
    def operation(self):
        """
        Every X seconds is checked if anomalies are happening
        from anonymous interaction (submission/file/comments/whatever flood)
        If the alarm has been raise, logs in the DB the event.

        This copy data inside StatisticsSchedule.RecentAnomaliesQ
        """
        yield Alarm.compute_activity_level()


def get_anomalies():
    anomalies = []
    for when, anomaly_blob in dict(StatisticsSchedule.RecentAnomaliesQ).iteritems():
        anomalies.append(
            [ when, anomaly_blob[0], anomaly_blob[1] ]
        )
    return anomalies

def clean_anomalies():
    StatisticsSchedule.RecentAnomaliesQ = dict()

def get_statistics():
    statsummary = {}

    for descblob in StatisticsSchedule.RecentEventQ:
        # descblob format:
        #  {  'id' : expired_event.event_id
        #     'when' : datetime_to_ISO8601(expired_event.creation_date)[:-8],
        #     'event' : expired_event.event_type, 'duration' :   }
        if 'event' not in descblob:
            continue
        statsummary.setdefault(descblob['event'], 0)
        statsummary[descblob['event']] += 1

    return statsummary



class StatisticsSchedule(GLJob):
    """
    Statistics just flush two temporary queue and store them
    in the database.
    """

    collection_start_datetime = datetime_now()
    RecentEventQ = []
    RecentAnomaliesQ = {}

    @staticmethod
    def reset():
        StatisticsSchedule.RecentEventQ = []
        StatisticsSchedule.RecentAnomaliesQ = {}

    @defer.inlineCallbacks
    def operation(self):
        """
        executed every 60 minutes
        """

        # ------- Anomalies section ------
        anomalies_to_save = get_anomalies()
        yield save_anomalies(anomalies_to_save)
        clean_anomalies()
        # ------- END of Anomalies section ------

        current_time = datetime_now()
        statistic_summary = get_statistics()

        yield save_statistics(StatisticsSchedule.collection_start_datetime,
                              current_time, statistic_summary)

        StatisticsSchedule.reset()
        StatisticsSchedule.collection_start_datetime = current_time

        log.debug("Saved stats and time updated, keys saved %d" %
                  len(statistic_summary.keys()))


class ResourceChecker(GLJob):
    """
    ResourceChecker is a scheduled job that verify the available
    resources in the GlobaLeaks box.
    At the moment is implemented only a monitor for the disk space,
    because the files that might be uploaded depend directly from
    this resource.
    """

    @classmethod
    def get_free_space(cls):
        statvfs = os.statvfs(GLSetting.working_path)
        free_mega_bytes = statvfs.f_frsize * statvfs.f_bavail / (1024 * 1024)
        return free_mega_bytes

    def operation(self):
        free_mega_bytes = ResourceChecker.get_free_space()

        alarm = Alarm()
        alarm.report_disk_usage(free_mega_bytes)
