import json

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from apps.quickstart.models import Course, Person

#
# Unit Test
#


class CourseUnitTests(TestCase):

    def setUp(self):
        Course.objects.create(name='python', price=300)
        Course.objects.create(name='java', price=500)

    def test_get_settings(self):
        # from config import settings
        from django.conf import settings
        self.assertEqual(settings.IS_DEBUG, True)
        self.assertEqual(settings.LOG_LEVEL, 'DEBUG')

    def test_create_course(self):
        self.assertEqual(Course.objects.count(), 2)

    def test_get_course(self):
        py = Course.objects.get(name='python')
        print(py)
        self.assertEqual(py.price, 300)

#
# Api Test
#


class CourseApiTests(APITestCase):

    def setUp(self):
        Course.objects.create(name='python', price=300)
        Course.objects.create(name='java', price=500)

    def test_list_courses(self):
        url = '/courses/free/'
        response = self.client.get(url, data={'max_price': 400})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expect_data = {'name': 'python', 'price': 300}
        self.assertEqual(get_response_results(response)[0], expect_data)


class PersonApiTest(APITestCase):

    def setUp(self):
        Person.objects.create(name='foo', age=33,
                              birthday='1983-7-1', role='qa', language='python')
        Person.objects.create(name='bar', age=35,
                              birthday='1981-10-9', role='dev', language='java')
        Person.objects.create(name='henry', age=24,
                              birthday='1991-3-14', role='qa', language='python')

    def test_create_person(self):
        self.assertEqual(Person.objects.count(), 3)

    def test_list_person(self):
        url = '/quickstart/person/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = get_response_results(response)
        self.assertEqual(len(results), 3)
        # print('list person:\n', results)

    def test_filter_person_failed(self):
        url = '/quickstart/person/by-filter/'
        # miss one query field
        response = self.client.post(url, data={"role": "qa"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print(response.content)

        # invalid age
        response = self.client.post(url, data={"role": "qa", "age": 20})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print(response.content)

    def test_filter_person_ok(self):
        url = '/quickstart/person/by-filter/'
        # ok
        response = self.client.post(url, data={"role": "qa", "age": 30})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = json.loads(response.content)
        self.assertEqual(len(results), 1)

        expect_data = {"id": "3", "name": "henry", "age": 24,
                       "birthday": "1991-03-14", "role": "qa", "language": "python"}
        self.assertEqual(results[0], expect_data)

    def test_filter_person_by_birthday_range(self):
        url = '/quickstart/person/by-filter/'
        response = self.client.get(
            url, data={'start': '1980-1-1', 'end': '1986-12-10'})
        results = json.loads(response.content)
        self.assertEqual(len(results), 2)
        print('by birthday range results:\n', results)


def get_response_results(response):
    resp_content = json.loads(response.content)
    return resp_content['results']
