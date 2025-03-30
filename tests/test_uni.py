from tests import client

class TestGet:
    def test_post_w(self):
        create_promo = {"wallet_address": "TMzoZ7iRvSJhi47Fygp47MQbVPbsezdqZV"}
        response = client.post(
            "/wallets/create-or-update",
            json=create_promo,
        )
        assert response.status_code == 200

    def test_get_w(self):
        response = client.get(
            "/wallets/get?page=1&page_size=1"
        )
        assert response.status_code == 200
        response_data = response.json()
        assert "total_pages" in response_data
        assert "current_page" in response_data
        assert "data" in response_data
        assert len(response_data["data"]) > 0