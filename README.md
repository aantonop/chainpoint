# chainpoint

[![Build Status](https://travis-ci.org/Storj/chainpoint.svg)](https://travis-ci.org/Storj/chainpoint?branch=master)
[![Coverage Status](https://coveralls.io/repos/Storj/chainpoint/badge.svg?branch=master&service=github)](https://coveralls.io/github/Storj/chainpoint?branch=master)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/storj/dataserv/master/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/storj/chainpoint.svg)](https://github.com/storj/chainpoint/issues)

# What is this?

We want to prove some data existed at a certain point and time, we call this
Proof of Existence. We can do that by finding the cryptographic hash of some data, then
inserting that hash into the Bitcoin blockchain. Since the Bitcoin blockchain is an immutable
and secure public ledger, we can prove that the data existed at the time of insertion, like a
mathematical notary. Unfortunately that insertion costs money, around $0.03, so it
becomes expensive if I wanted to do this for 10,000+ documents. 

Instead we can take that data and put it in a 
[Merkle tree](https://en.wikipedia.org/wiki/Merkle_tree), and insert the Merkle root into
the Bitcoin blockchain. For any of the items in the Merkle tree, as long as we have the Merkle proof,
we can prove that it is contained in that Merkle root notarized in the Bitcoin blockchain. 

Therefore we can notarize 10,000 documents for $0.03 instead of $300. It is 
recommended that the party notarizing their document or data hold on to the Merkle proof "receipt." 
This allows that party to prove that their document has been notarized in a specific Bitcoin transaction
in the absence of any other data.

**tldr;** A federated server for building blockchain notarized Merkle trees, and returning the Merkle
proof as a receipt. 


# Chainpoint Standard Receipt
A standardized Chainpoint receipt format allows any system to verify a receipt by checking a Bitcoin transaction and
using math to verify the data. 

### Table Breakdown
|  Header |   |
|---|---|
| chainpoint_version | version of the Chainpoint standard  |
| hash_type | hashing algorithm used to encrypt target data (sha-256) |
| merkle_root |  root of the Merkle Tree that is published in the blockchain  |
| tx_id | transaction id where the Merkle Root is stored |
| timestamp  | non-authoritative Unix timestamp of the target |

|  Target |   |
|---|---|
| target_hash | hash of the target that is being recorded in the blockchain  |
| target_proof | Merkle proof used to prove target_hash is part of Merkle tree |
| URI (optional) |  path to the target  |

|  Extra |   |
|---|---|
| custom (optional) | hash of the target that is being recorded in the blockchain  |
| ... | ... |

### Sample JSON
```json
{
    "header": {
        "chainpoint_version": "1.0",
        "hash_type": "SHA-256",
        "merkle_root": "6a9a3c86d47f1fe12648c86368ecd9723ff12e3fc34f6ae219d4d9d3e0d60667",
        "tx_id": "012fdc0eb5ebae181e1197b4e9307731473118b0634d3ede749a562e9d11809e",
        "local_timestamp": "1436172703"
    },
    "target": {
        "target_hash": "2f7f9092b2d6c5c17cfe2bcf33fc38a41f2e4d4485b198c2b1074bba067e7168",
        "target_URI": "http://blockchainreciept.com/target_name",
        "target_proof": [
            {
                "left": "e1566f09e0deea437826514431be6e4bdb4fe10aa54d75aecf0b4cdc1bc4320c",
                "parent": "0fdd6b6895e15115c262f6acb9a6ae0c73248568b740454ab21591f8a533dd7f",
                "right": "2f7f9092b2d6c5c17cfe2bcf33fc38a41f2e4d4485b198c2b1074bba067e7168"
            },
            {
                "left": "0fdd6b6895e15115c262f6acb9a6ae0c73248568b740454ab21591f8a533dd7f",
                "parent": "6a9a3c86d47f1fe12648c86368ecd9723ff12e3fc34f6ae219d4d9d3e0d60667",
                "right": "3b7546ed79e3e5a7907381b093c5a182cbf364c5dd0443dfa956c8cca271cc33"
            }
        ]
    },
    "extra": [
        { "custom_key_1": "value_1"},
        { "custom_key_2": "value_2"}
    ]
}
```

# Chainpoint Standard Block
A standardized Chainpoint block is a collection of data items which are summarized and inserted into the Bitcoin
blockchain. 

### Table Breakdown
|  Block |   |
|---|---|
| block_num | number of block on local database  |
| closed | can more data items be added to this block |
| leaves |  list of hash of all the data items in this block  |
| merkle_root | the cryptographic summary of all the data items in the block |
| tx_id  | bitcoin transaction id in which the merkle_root was included |

### Sample JSON

    {
        "block_num": 1,
        "closed": true,
        "leaves": [
            "e1566f09e0deea437826514431be6e4bdb4fe10aa54d75aecf0b4cdc1bc4320c",
            "2f7f9092b2d6c5c17cfe2bcf33fc38a41f2e4d4485b198c2b1074bba067e7168",
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        ],
        "merkle_root": "6a9a3c86d47f1fe12648c86368ecd9723ff12e3fc34f6ae219d4d9d3e0d60667",
        "tx_id": "012fdc0eb5ebae181e1197b4e9307731473118b0634d3ede749a562e9d11809e"
    }
