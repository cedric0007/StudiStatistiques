from app import fake_hash_password, fake_decode_token, UserInDB, get_current_user, get_current_active_user, get_depenses, fonction_total_spending_by_category
from unittest import TestCase, main
import asyncio

class TestApplication(TestCase):

    def test_fake_hash_password(self):
        self.assertEqual(fake_hash_password("test"), "fakehashedtest")

    def test_fake_decode_token(self):
         self.assertIsInstance(fake_decode_token("johndoe"), UserInDB)

    # def test_get_depenses(self):
    #     self.assertEqual(get_depenses(),"1000")

    def test_fonction_total_spending_by_category(self):
        # self.assertEqual(fonction_total_spending_by_category(),"1000")
        self.assertIsInstance(fonction_total_spending_by_category(),list)
    # def test_get_current_user(self):
    #     # user = asyncio.run(self.get_current_user())
    #     # self.assertIsInstance(user, UserInDB)
    #     self.assertIsInstance(get_current_user("johndoe"), UserInDB)

    # def test_get_current_active_user(self):
    #     self.assertIsInstance(get_current_active_user("test"), UserInDB)

main()

# python app_test.py -v ==> lancer les test présents
# coverage run app_test.py 
# coverage report
# coverage html