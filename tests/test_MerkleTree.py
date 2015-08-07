import json
import unittest

from chainpoint.MerkleTree import sha256
from chainpoint.MerkleTree import is_sha256
from chainpoint.MerkleTree import MerkleTree
from chainpoint.MerkleTree import MerkleBranch
from chainpoint.MerkleTree import MerkleProof


class MerkleTreeTest(unittest.TestCase):
    # testing sha256 hashing
    def test_sha256(self):
        result1 = sha256("test")
        result2 = sha256("test2")

        ans1 = '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08'
        ans2 = '60303ae22b998861bce3b28f33eec1be758a213c86c93c076dbe9f558c11c752'

        self.assertEqual(result1, ans1)
        self.assertEqual(result2, ans2)

        self.assertTrue(is_sha256(result1))
        self.assertTrue(is_sha256(result2))

    def test_is_sha256(self):
        valid_hash = '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08'
        self.assertTrue(is_sha256(valid_hash))

        invalid_hash = 'notarealhash'
        self.assertFalse(is_sha256(invalid_hash))

        invalid_hash = '---'
        self.assertFalse(is_sha256(invalid_hash))

    # testing MerkleBranch
    def test_merkle_branch(self):
        left = sha256("test")
        right = sha256("test2")
        branch = MerkleBranch(left, right)

        left_hash = '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08'
        right_hash = '60303ae22b998861bce3b28f33eec1be758a213c86c93c076dbe9f558c11c752'
        parent = '694299f8eb01a328732fb21f4163fbfaa8f60d5662f04f52ad33bec63953ec7f'

        expected_json = {
            "parent": parent,
            "left": left_hash,
            "right": right_hash,
        }

        # test parent and json output
        self.assertEqual(branch.get_parent(), parent)
        self.assertEqual(branch.get_json(), expected_json)

    # testing MerkleTree
    def test_two_even_items(self):
        tree = MerkleTree()

        tree.add_content("test")
        tree.add_hash(tree.hash_f("test2"))

        ans = '694299f8eb01a328732fb21f4163fbfaa8f60d5662f04f52ad33bec63953ec7f'
        self.assertEqual(tree.merkle_root(), ans)

    def test_tree_odd_items(self):
        tree = MerkleTree()

        tree.add_content("test")
        tree.add_content("test2")
        tree.add_content("test3")

        ans = 'd49e815a91a26d399f8c2fba429e6ef7e472e54b6eb1e04341d207eee219f6c0'
        self.assertEqual(tree.merkle_root(), ans)

    def test_large_tree(self):
        tree = MerkleTree()
        for i in range(10000):
            tree.add_content(str(i))

        ans = 'a048d580177b80a60cbd31355400a0c9eabb5d2d3a4704fc9c86bae277f985c7'
        self.assertEqual(tree.merkle_root(), ans)

    # testing MerkleProof
    def test_proof_true(self):
        tree = MerkleTree()

        tree.add_content("test")
        tree.add_content("test2")
        tree.add_content("test3")

        proof = tree.merkle_proof(sha256("test"))
        self.assertTrue(proof.is_valid())

    def test_proof_false(self):
        tree = MerkleTree()

        tree.add_content("test1")
        tree.add_content("test2")
        tree.add_content("test3")

        proof = tree.merkle_proof(sha256("test"))
        self.assertFalse(proof.is_valid())

    def test_proof_single_true(self):
        tree = MerkleTree()
        tree.add_content("test")
        proof = tree.merkle_proof(sha256("test"))
        self.assertTrue(proof.is_valid())

    def test_proof_single_false(self):
        tree = MerkleTree()
        tree.add_content("test")
        proof = tree.merkle_proof(sha256("test9"))
        self.assertFalse(proof.is_valid())

    def test_merkle_proof_simple_true(self):
        tree = MerkleTree()
        tree.add_content("test")
        tree.add_content("test2")

        left = sha256("test")
        right = sha256("test2")
        branch = MerkleBranch(left, right)

        target = left
        proof = MerkleProof(target, tree)
        proof.add(branch)
        self.assertTrue(proof.is_valid())

    def test_merkle_proof_simple_false(self):
        tree = MerkleTree()
        tree.add_content("test")
        tree.add_content("test2")

        left = sha256("test")
        right = sha256("test2")
        branch = MerkleBranch(left, right)

        target = sha256("notinproof")
        proof = MerkleProof(target, tree)
        proof.add(branch)
        self.assertFalse(proof.is_valid())

    def test_proof_get_json(self):
        tree = MerkleTree()

        tree.add_content("test")
        tree.add_content("test2")
        tree.add_content("test3")

        proof = tree.merkle_proof(sha256("test"))
        json_data = json.loads(proof.get_json())

        self.assertEqual(json_data[0]["right"], '60303ae22b998861bce3b28f33eec1be758a213c86c93c076dbe9f558c11c752')
        self.assertEqual(json_data[0]["left"], '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08')
        self.assertEqual(json_data[0]["parent"], '694299f8eb01a328732fb21f4163fbfaa8f60d5662f04f52ad33bec63953ec7f')

        self.assertEqual(json_data[1]["right"], '000b7a5fc83fa7fb1e405b836daf3488d00ac42cb7fc5a917840e91ddc651661')
        self.assertEqual(json_data[1]["left"], '694299f8eb01a328732fb21f4163fbfaa8f60d5662f04f52ad33bec63953ec7f')
        self.assertEqual(json_data[1]["parent"], 'd49e815a91a26d399f8c2fba429e6ef7e472e54b6eb1e04341d207eee219f6c0')
