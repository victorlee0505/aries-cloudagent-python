import pytest
from asynctest import mock as async_mock

from ......messaging.request_context import RequestContext
from ......core.profile import Profile
from ......messaging.responder import MockResponder

from ...handlers import transaction_cancel_handler as handler
from ...messages.cancel_transaction import CancelTransaction
from ......connections.models.conn_record import ConnRecord


@pytest.fixture()
async def request_context() -> RequestContext:
    ctx = RequestContext.test_context()
    yield ctx


@pytest.fixture()
async def profile(request_context) -> Profile:
    yield await request_context.profile


class TestTransactionCancelHandler:
    @pytest.mark.asyncio
    @async_mock.patch.object(handler, "TransactionManager")
    async def test_called(self, mock_tran_mgr, request_context):
        mock_tran_mgr.return_value.receive_cancel_transaction = (
            async_mock.CoroutineMock()
        )
        request_context.message = CancelTransaction()
        request_context.connection_record = ConnRecord(
            connection_id="b5dc1636-a19a-4209-819f-e8f9984d9897"
        )
        handler_inst = handler.TransactionCancelHandler()
        responder = MockResponder()
        await handler_inst.handle(request_context, responder)
        mock_tran_mgr.return_value.receive_cancel_transaction.assert_called_once_with(
            request_context.message, request_context.connection_record.connection_id
        )
