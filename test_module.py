import unittest
from module import Source, compare_price, compare_dates
class ComparisonTests(unittest.TestCase):
    def price(self, a="10", b="10.10", **kw):
        args=dict(left_currency="USD", right_currency="USD", tolerance="0.10", sources=(Source("quote-demo","line-1","unit_price"),Source("po-demo","line-1","unit_price")))
        return compare_price(a,b,**{**args,**kw})
    def test_decimal_boundary(self): self.assertEqual(self.price().reason,"within tolerance")
    def test_price_delta(self): self.assertEqual(self.price(b="11").delta,"1")
    def test_currency_no_implicit_conversion(self): self.assertEqual(self.price(right_currency="EUR").status,"REVIEW_REQUIRED")
    def test_missing_not_zero(self): self.assertEqual(self.price(a=None).status,"UNVERIFIABLE")
    def test_invalid_amounts(self):
        for value in ("NaN","Infinity","-1"):
            with self.subTest(value=value), self.assertRaises(ValueError): self.price(a=value)
    def test_dates(self):
        self.assertEqual(compare_dates("2026-01-01","2026-01-03",tolerance_days=2),"WITHIN_TOLERANCE")
        self.assertEqual(compare_dates("2026-01-01","2026-01-04",tolerance_days=2),"OUTSIDE_TOLERANCE")
    def test_missing_date(self): self.assertEqual(compare_dates(None,"2026-01-03",tolerance_days=0),"UNVERIFIABLE")
    def test_provenance_required(self):
        with self.assertRaises(ValueError): Source("", "line-1", "price")
if __name__ == "__main__": unittest.main()
