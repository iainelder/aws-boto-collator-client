# AWS Boto Collator Client

A wrapper for a boto3 client that collates each paginated API call into a single result.

For anything else, like non-method attributes or non-pagianted API methods, it returns the same result as the wrapped client.

The AWS CLI conveniently collates automatically. If you naively translate an AWS CLI command to to boto3 method call, you might be surprised when you get less results than you were expecting for a long list of resources.

Use this wrapper to collate automatically whenever it would be necessary to get the full result.

It should be a drop-in replacement for a normal client.

## Deprecation Notice

I don't use this library any more because it doesn't work with type hints and I don't see any easy way to make it so.

Instead I replicate its functionality where I would use it with a list comprehension. Here's an example using the Security Hub DescribeStandards API.

```python
sh = session.client("securityhub")
available_standards = [
    standard
    for page in sh.get_paginator("describe_standards").paginate()
    for standard in page["Standards"]
]
```

## Installation

The collator client is published to PyPI as boto-collator-client, so you can install it with pip or anything equivalent.

```bash
pip install boto-collator-client
```

## Example

Given an AWS organization with more than 20 accounts, and a file count_accounts.py with the following content:

```python
import boto3

from boto_collator_client import CollatorClient

boto_org = boto3.Session().client("organizations")
boto_result = len(boto_org.list_accounts()["Accounts"])
print(f"Boto result: {boto_result}")

collator_org = CollatorClient(boto_org)
collator_result = len(collator_org.list_accounts()["Accounts"])
print(f"Collator result: {collator_result}")
```

You should see output like this:

```text
$ python count_accounts.py
Boto result: 20
Collator result: 66
```

The collator result will match the number of accounts in the org no matter how many pages of results there are.

## Development

Use Poetry to build and publish a new version to PyPI:

```bash
poetry build
poetry publish
```

## See also

[BBP - Better Boto Paginator](https://github.com/mdavis-xyz/bbp) provides a neat way to iterate over all the resources from a paginated boto3 API.
