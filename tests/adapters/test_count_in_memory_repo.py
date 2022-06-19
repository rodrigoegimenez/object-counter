from counter.adapters.count_repo import CountInMemoryRepo
from counter.domain.models import ObjectCount


class TestCountInMemoryRepo:
    def test_repo_inits_empty(self):
        repo = CountInMemoryRepo()
        values = repo.read_values()
        assert len(values) == 0

    def test_reads_all_values(self):
        repo = CountInMemoryRepo()
        values = [
            ObjectCount(object_class="cat", count=1),
            ObjectCount(object_class="dog", count=2),
        ]
        repo.update_values(values)
        inserted_values = repo.read_values()
        assert values == inserted_values

    def test_reads_specified_values(self):
        repo = CountInMemoryRepo()
        values = [
            ObjectCount(object_class="cat", count=1),
            ObjectCount(object_class="dog", count=2),
        ]
        repo.update_values(values)
        inserted_values = repo.read_values(object_classes=["cat"])
        assert [
            value for value in values if value.object_class == "cat"
        ] == inserted_values
