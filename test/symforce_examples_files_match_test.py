from pathlib import Path

from symforce import types as T
from symforce.test_util import TestCase

CURRENT_DIR = Path(__file__).parent
SYMFORCE_DIR = CURRENT_DIR.parent
EXAMPLES_DIR = SYMFORCE_DIR.joinpath("symforce", "examples")


class ExampleFilesMatchTest(TestCase):
    def check_path(
        self, example1: Path, example2: Path, path: str, replacer: T.Callable[[str], str]
    ) -> None:
        with open(example2.joinpath(path)) as f:
            example2_data = replacer(f.read())

        self.compare_or_update(
            path=example1.joinpath(path), data=example2_data,
        )

    def test_equivalent_files_are_identical(self) -> None:
        """
        Test that copies of the same file in different examples are identical
        """
        fixed_size_example_dir = EXAMPLES_DIR.joinpath("bundle_adjustment_fixed_size")
        dynamic_size_example_dir = EXAMPLES_DIR.joinpath("bundle_adjustment_dynamic_size")

        replacer = lambda text: text.replace(
            "bundle_adjustment_dynamic_size", "bundle_adjustment_fixed_size"
        )
        self.check_path(
            fixed_size_example_dir, dynamic_size_example_dir, "build_example_state.cc", replacer
        )
        self.check_path(
            fixed_size_example_dir, dynamic_size_example_dir, "build_example_state.h", replacer
        )


if __name__ == "__main__":
    ExampleFilesMatchTest.main()
