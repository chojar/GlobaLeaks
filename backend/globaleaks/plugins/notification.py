# -*- coding: UTF-8
#
# Notification
# ************
#
# This is in fact Mail Notification Plugin, that supports the simplest Mail notification
# operations.
# When new Notification/Delivery will starts to exists, this code would come back to be
# one of the various plugins (used by default, but still an optional adoptions)

from globaleaks.utils.utility import log
from globaleaks.utils.mailutils import sendmail, MIME_mail_build
from globaleaks.utils.templating import Templating
from globaleaks.plugins.base import Notification
from globaleaks.security import GLBGPG
from globaleaks.models import Receiver
from globaleaks.settings import GLSetting

class MailNotification(Notification):

    plugin_name = u'Mail'
    plugin_type = u'notification'
    plugin_description = u"Mail notification, with encryption supports"

    # This declaration is not more used, because hardcoded
    # admin_fields = {'server' : 'text', 'port': 'int', 'password' : 'text', 'username':'text', 'ssl' : 'bool' }
    # receiver_fields = {'mail_address' : 'text'}
    # But at the first presence of a different notification plugin, need to be resumed and
    # integrated in the validation messages.

    def validate_admin_opt(self, pushed_ao):
        fields = ['server', 'port', 'username', 'password']
        if all(field in pushed_ao for field in fields):
            return True
        else:
            return False

    def validate_receiver_opt(self, admin_fields, receiver_fields):
        log.debug("[%s] receiver_fields %s (with admin %s)" % ( self.__class__.__name__, receiver_fields, admin_fields))
        return True

    def do_notify(self, event):
        if not self.validate_admin_opt(event.notification_settings):
            log.info('invalid mail settings for admin')
            return None

        # At the moment the language used is a system language, not
        # Receiver preferences language ?
        if event.type == u'encrypted_tip':
            body = Templating().format_template(
                event.notification_settings['encrypted_tip_template'], event)
            title = Templating().format_template(
                event.notification_settings['encrypted_tip_mail_title'], event)
        elif event.type == u'plaintext_tip':
            body = Templating().format_template(
                event.notification_settings['plaintext_tip_template'], event)
            title = Templating().format_template(
                event.notification_settings['plaintext_tip_mail_title'], event)
        elif event.type == u'encrypted_file':
            body = Templating().format_template(
                event.notification_settings['encrypted_file_template'], event)
            title = Templating().format_template(
                event.notification_settings['encrypted_file_mail_title'], event)
        elif event.type == u'plaintext_file':
            body = Templating().format_template(
                event.notification_settings['plaintext_file_template'], event)
            title = Templating().format_template(
                event.notification_settings['plaintext_file_mail_title'], event)
        elif event.type == u'encrypted_comment':
            body = Templating().format_template(
                event.notification_settings['encrypted_comment_template'], event)
            title = Templating().format_template(
                event.notification_settings['encrypted_comment_mail_title'], event)
        elif event.type == u'plaintext_comment':
            body = Templating().format_template(
                event.notification_settings['plaintext_comment_template'], event)
            title = Templating().format_template(
                event.notification_settings['plaintext_comment_mail_title'], event)
        elif event.type == u'encrypted_message':
            body = Templating().format_template(
                event.notification_settings['encrypted_message_template'], event)
            title = Templating().format_template(
                event.notification_settings['encrypted_message_mail_title'], event)
        elif event.type == u'plaintext_message':
            body = Templating().format_template(
                event.notification_settings['plaintext_message_template'], event)
            title = Templating().format_template(
                event.notification_settings['plaintext_message_mail_title'], event)
        else:
            raise NotImplementedError("At the moment, only Tip expected")

        # If the receiver has encryption enabled (for notification), encrypt the mail body
        if event.receiver_info['gpg_key_status'] == u'enabled':

            gpob = GLBGPG()
            try:
                gpob.load_key(event.receiver_info['gpg_key_armor'])
                body = gpob.encrypt_message(event.receiver_info['gpg_key_fingerprint'], body)
            except Exception as excep:
                log.err("Error in GPG interface object (for %s: %s)! (notification+encryption)" %
                        (event.receiver_info['username'], str(excep) ))
                return None # We return None and the mail will be delayed
                            # If GPG is enabled and the key is invalid this
                            # is the only possiibly thing to do.
                            # The PGP check schedule will disable the key
                            # and alert the user and the admin
            finally:
                # the finally statement is always called also if
                # except contains a return or a raise
                gpob.destroy_environment()

        receiver_mail = event.receiver_info['mail_address']

        # XXX here can be catch the subject (may change if encrypted or whatever)
        message = MIME_mail_build(GLSetting.memory_copy.notif_source_name,
                                  GLSetting.memory_copy.notif_source_email,
                                  event.receiver_info['name'],
                                  receiver_mail,
                                  title,
                                  body)

        return self.mail_flush(event.notification_settings['source_email'],
                               [receiver_mail], message, event)


    @staticmethod
    def mail_flush(from_address, to_address, message_file, event):
        """
        This function just wrap the sendmail call, using the system memory variables.
        """
        log.debug('Email: connecting to [%s:%d] to notify %s using [%s]' %
                  (GLSetting.memory_copy.notif_server,
                   GLSetting.memory_copy.notif_port,
                   to_address[0], GLSetting.memory_copy.notif_security))

        return sendmail(authentication_username=GLSetting.memory_copy.notif_username,
                        authentication_password=GLSetting.memory_copy.notif_password,
                        from_address= from_address,
                        to_address= to_address,
                        message_file=message_file,
                        smtp_host=GLSetting.memory_copy.notif_server,
                        smtp_port=GLSetting.memory_copy.notif_port,
                        security=GLSetting.memory_copy.notif_security,
                        event=event)

