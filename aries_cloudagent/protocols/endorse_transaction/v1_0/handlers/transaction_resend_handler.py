"""Transaction resend handler."""

from .....messaging.base_handler import (
    BaseHandler,
    BaseResponder,
    RequestContext,
)

from ..manager import TransactionManager, TransactionManagerError
from ..messages.transaction_resend import TransactionResend


class TransactionResendHandler(BaseHandler):
    """Handler class for transaction resend."""

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """
        Handle transaction resend.

        Args:
            context: Request context
            responder: Responder callback
        """

        self._logger.debug(f"TransactionResendHandler called with context {context}")
        assert isinstance(context.message, TransactionResend)

        profile_session = await context.session()
        mgr = TransactionManager(profile_session)
        try:
            await mgr.receive_transaction_resend(
                context.message, context.connection_record.connection_id
            )
        except TransactionManagerError:
            self._logger.exception("Error receiving resend transaction request")
