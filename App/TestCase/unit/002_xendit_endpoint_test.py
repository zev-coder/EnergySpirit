from unittest.mock import patch, Mock
from uuid import UUID

from App.DB.dependencies.Xendit.xendit_payment_logic import create_invoice


@patch("App.DB.dependencies.Xendit.xendit_payment_logic.requests.post")
def test_create_invoice(mock_post):

    mock_response = Mock()

    mock_response.status_code = 201
    mock_response.json.return_value = {
        "external_id": "ORDER-Product-12345678-1234-5678-1234-567812345678",
        "amount_id": 10000,
        "payer_email": "john@example.com",
        "invoice_url": "https://checkout.xendit.co/web/123",
        "status": "PENDING",
    }

    mock_post.return_value = mock_response
    order_id = UUID("12345678-1234-5678-1234-567812345678")
    mock_settings = Mock(XENDIT_SECRET_API="test-secret")

    with patch(
        "App.DB.dependencies.Xendit.xendit_payment_logic.get_settings",
        return_value=mock_settings,
    ):
        result = create_invoice(
            product="product",
            external_id="ignored-input",
            amount_id=10000,
            payer_email="john@example.com",
            description="Test",
            currency="IDR",
            order_id=order_id,
        )

    assert result.uuid == order_id
    assert result.external_id == "ORDER-Product-12345678-1234-5678-1234-567812345678"
    assert result.amount_id == 10000
    assert result.payer_email == "john@example.com"
    assert result.invoice_url == "https://checkout.xendit.co/web/123"
    assert result.status == "PENDING"
    mock_post.assert_called_once()
    assert mock_post.call_args.kwargs["json"] == {
        "external_id": "ORDER-Product-12345678-1234-5678-1234-567812345678",
        "amount_id": 10000.0,
        "payer_email": "john@example.com",
        "description": "Test",
        "currency": "IDR",
    }
    assert mock_post.call_args.kwargs["headers"]["Authorization"] == "Basic dGVzdC1zZWNyZXQ6"
