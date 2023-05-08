from app import fake_hash_password, fake_decode_token, UserInDB, get_current_user, get_current_active_user,  get_total_spending_by_category, get_total_depensesParCsp, get_total_depensesParCategorie
from unittest import TestCase, main

class TestApplication(TestCase):

    def test_fake_hash_password(self):
        self.assertEqual(fake_hash_password("test"), "fakehashedtest")

    def test_fake_decode_token(self):
         self.assertIsInstance(fake_decode_token("johndoe"), UserInDB)

    def test_get_total_spending_by_category(self):
        self.assertIsInstance(get_total_spending_by_category(),list)

    def test_get_total_depensesParCsp(self):
        self.assertIsInstance(get_total_depensesParCsp(),list)

    def test_get_total_depensesParCategorie(self):
        self.assertIsInstance(get_total_depensesParCategorie(),list)


main()

# python app_test.py -v ==> lancer les test présents
# coverage run app_test.py 
# coverage report
# coverage html