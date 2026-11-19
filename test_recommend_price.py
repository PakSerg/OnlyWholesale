import asyncio
import unittest
from decimal import Decimal

from starter import recommend_price, sample_fetch_offers


class RecommendPriceTest(unittest.IsolatedAsyncioTestCase):
    async def test_regular_calculation(self):
        result = await recommend_price(
            sample_fetch_offers,
            Decimal("4900.00"),
            Decimal("4500.00"),
        )
        self.assertEqual(result["price"], Decimal("4728.00"))
        self.assertEqual(result["decision"], "APPLY")

    async def test_timeout_keeps_current_price(self):
        async def fetch_offers():
            await asyncio.sleep(5)
            return {"status": "success", "offers": []}

        result = await recommend_price(
            fetch_offers,
            Decimal("4900.00"),
            Decimal("4500.00"),
            timeout_s=0.05,
        )
        self.assertEqual(result["price"], Decimal("4900.00"))
        self.assertEqual(result["decision"], "HOLD")


if __name__ == "__main__":
    unittest.main()
