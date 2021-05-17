#  Copyright (c) 2021 Arbetsförmedlingen.

from odoo import models, api, fields
from odoo.sql_db import db_connect

import logging
_logger = logging.getLogger(__name__)


class MaxTriesExceededError(Exception):
    pass


class AFProcessLog(models.Model):
    _name = "af.process.log"
    _description = "AF Process Log"
    _rec_name = 'eventid'
    _sql_constraints = [("af_sync_log_messageId_unique",
                         "unique(messageId, process)",
                         "Message Id must be unique within a process.")]

    process = fields.Char(string="Process", required=True)
    eventid = fields.Char(string="Event Id", required=True, index=True)
    step = fields.Char(string="Step", required=True)
    message = fields.Text(string="Message", required=True)
    error_message = fields.Text(string='Error Message')
    status = fields.Boolean(string="Status")
    no_tries = fields.Integer(string="No. of tries")
    objectid = fields.Char(string="Object Id")
    info_1 = fields.Text(string="Informational Message 1", required=False)
    info_2 = fields.Text(string="Informational Message 2", required=False)
    info_3 = fields.Text(string="Informational Message 3", required=False)

    @api.model
    def log_message(self, process, eventid, step, message=None, error_message=None,
                    status=True, objectid=None, first=False, info_1=None, info_2=None, info_3=None, **kwargs):
        """ Log a message.
        :param process: The name of the process.
        :param eventid: The id of the logged event.
        :param step: The step in the process.
        :param message: The log message.
        :param error_message: An error message.
        :param status: The status of the event.
        :param first: True if this is the first step of the event
                      chain. Will cause no_tries to increment.
        :param objectid: The id of the object the event concerns.
        """
        # Log with new cursor to avoid any rollback issues
        db = db_connect(self.env.cr.dbname)
        max_tries_exceeded = False
        try:
            with db.cursor() as cr:
                with api.Environment.manage():
                    env = api.Environment(cr, self.env.uid, {})
                    log = env["af.process.log"].search([("process", "=", process), ("eventid", "=", eventid)])
                    if not log:
                        env["af.process.log"].create({
                            "process": process,
                            "eventid": eventid,
                            "step": step,
                            "message": message,
                            "error_message": error_message,
                            "status": status,
                            "objectid": objectid,
                            "no_tries": 1,
                        })
                    elif log.no_tries >= int(env['ir.config_parameter'].get_param(
                            'af_process_log.max_tries', '10')):
                        max_tries_exceeded = True
                    else:
                        vals = {
                            "process": process,
                            "eventid": eventid,
                            "step": step,
                            "error_message": error_message,
                            "status": status,
                        }
                        if message:
                            vals["message"] = message
                        if objectid:
                            vals["objectid"] = objectid
                        if first:
                            vals["no_tries"] = log.no_tries + 1
                        if info_1:
                            vals["info_1"] = info_1
                        if info_2:
                            vals["info_2"] = info_2
                        if info_3:
                            vals["info_3"] = info_3
                        log.write(vals)
        except Exception:
            _logger.exception(f"Exception during message handling! process: {process}, eventId: {eventid}")
        if max_tries_exceeded:
            raise MaxTriesExceededError(f"Max retries have been reached! process: {process}, eventId: {eventid}")
