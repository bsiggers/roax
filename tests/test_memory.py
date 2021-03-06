
import roax.resource as r
import roax.schema as s
import unittest

from roax.memory import MemoryResource
from roax.resource import operation
from uuid import uuid4


class TestMemoryResource(unittest.TestCase):

    def test_crud_dict(self):
        
        _schema = s.dict({
            "id": s.uuid(required=False),
            "foo": s.str(),
            "bar": s.int(),
        })

        class FooResource(MemoryResource):

            @operation(params={"_body": _schema}, returns=s.dict({"id": _schema.properties["id"]}))
            def create(self, _body):
                return super().create(uuid4(), _body)

            @operation(params={"id": _schema.properties["id"]}, returns=_schema)
            def read(self, id):
                return {**super().read(id), "id": id}

            @operation(params={"id": _schema.properties["id"], "_body": _schema})
            def update(self, id, _body):
                return super().update(id, _body)

            @operation(params={"id": _schema.properties["id"]})
            def delete(self, id):
                return super().delete(id)

            @operation(type="query", returns=s.list(_schema.properties["id"]))
            def list(self):
                return super().list()

        rs = FooResource(dir)
        r1 = { "foo": "hello", "bar": 1 }
        id = rs.create(r1)["id"]
        r1["id"] = id
        r2 = rs.read(id)
        self.assertEqual(r1, r2) 
        r1["bar"] = 2
        rs.update(id, r1)
        r2 = rs.read(id)
        self.assertEqual(r1, r2) 
        rs.delete(id)
        self.assertEqual(rs.list(), [])


    def test_crud_str(self):

        _schema = s.str()

        class StrResource(MemoryResource):

            @operation(params={"id": s.str(), "_body": _schema}, returns=s.dict({"id": s.str()}))
            def create(self, id, _body):
                return super().create(id, _body)

            @operation(params={"id": s.str()}, returns=_schema)
            def read(self, id):
                return super().read(id)

            @operation(params={"id": s.str(), "_body": _schema})
            def update(self, id, _body):
                return super().update(id, _body)

            @operation(params={"id": s.str()})
            def delete(self, id):
                return super().delete(id)

            @operation(type="query", returns=s.list(s.str()))
            def list(self):
                return super().list()

        mr = StrResource()
        body = "你好，世界!"
        id = "hello_world"
        self.assertEqual(id, mr.create(id, body)["id"])
        self.assertEqual(mr.list(), [id])
        self.assertEqual(body, mr.read(id))
        body = "Goodbye world!"
        mr.update(id, body)
        self.assertEqual(body, mr.read(id))
        mr.delete(id)
        self.assertEqual(mr.list(), [])

    def test_crud_bytes(self):

        mr = MemoryResource(dir)
        body = b"\x00\x0e\0x01\0x01\0x00"
        id = "binary"
        self.assertEqual(id, mr.create(id, body)["id"])
        self.assertEqual(mr.list(), [id])
        self.assertEqual(body, mr.read(id))
        body = bytes((1,2,3,4,5))
        mr.update(id, body)
        self.assertEqual(body, mr.read(id))
        mr.delete(id)
        self.assertEqual(mr.list(), [])


if __name__ == "__main__":
    unittest.main()
