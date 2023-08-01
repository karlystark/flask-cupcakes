import os

os.environ["DATABASE_URL"] = 'postgresql:///cupcakes_test'

from unittest import TestCase

from app import app
from models import db, Cupcake, DEFAULT_IMAGE_URL

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()

CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image_url": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image_url": "http://test.com/cupcake2.jpg"
}


class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""

        Cupcake.query.delete()

        # "**" means "pass this dictionary as individual named params"
        cupcake = Cupcake(**CUPCAKE_DATA)
        db.session.add(cupcake)
        db.session.commit()

        self.cupcake_id = cupcake.id

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_list_cupcakes(self):
        """Tests GET route for all cupcakes - correct status code, correct JSON
        response"""

        with app.test_client() as client:
            resp = client.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcakes": [{
                    "id": self.cupcake_id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image_url": "http://test.com/cupcake.jpg"
                }]
            })

    def test_get_cupcake(self):
        """Tests GET route for cupcake - correct status code, correct JSON
        response"""

        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake_id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake_id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image_url": "http://test.com/cupcake.jpg"
                }
            })


    def test_create_cupcake(self):
        """Tests POST route, adding cupcake instance - correct status code,
        ID is integer, JSON response, and number of instances in database"""

        with app.test_client() as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 201)

            cupcake_id = resp.json['cupcake']['id']

            # don't know what ID we'll get, make sure it's an int
            self.assertIsInstance(cupcake_id, int)

            self.assertEqual(resp.json, {
                "cupcake": {
                    "id": cupcake_id,
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image_url": "http://test.com/cupcake2.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 2)


    def test_update_cupcake(self):
        """Tests PATCH route updating a cupcake instance - correct status code,
        correct JSON response"""

        with app.test_client() as client:
            url = "/api/cupcakes"

            post_resp = client.post(url, json=CUPCAKE_DATA)

            cupcake_id = post_resp.json['cupcake']['id']

            data_for_patch = {
                "rating": 300,
                "image_url": ""
            }

            patch_resp = client.patch(f"{url}/{cupcake_id}", json=data_for_patch)

            self.assertEqual(patch_resp.status_code, 200)

            self.assertEqual(patch_resp.json, {
                "cupcake": {
                    "id": cupcake_id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 300,
                    "image_url": DEFAULT_IMAGE_URL
                }
            })


    def test_delete_cupcake(self):
        """Tests delete route - correct status code, correct json response,
        and number of instances in test database after delete"""

        with app.test_client() as client:

            url = "/api/cupcakes"

            post_resp = client.post(url, json=CUPCAKE_DATA)

            # grab id from that created cupcake
            cupcake_id = post_resp.json['cupcake']['id']

            self.assertEqual(Cupcake.query.count(), 2)

            # use that id to delete the right cupcake
            delete_resp = client.delete(f"{url}/{cupcake_id}")

            self.assertEqual(Cupcake.query.count(), 1)

            self.assertEqual(delete_resp.status_code, 200)

            self.assertEqual(delete_resp.json, {
                "deleted": [cupcake_id]
            })






