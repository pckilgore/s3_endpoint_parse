# s3-endpoint-parse

Flexibly parses well-formed S3 URL/URIs, including legacy formats and new
fips / dualstack formats, and for Chinese (中国) regions.

Returns a dictionary describing the endpoint:

```python
{
  "match": bool       # True if library matched
  "protocol": string  # May be empty
  "bucket": string    # Set if match is True
  "key": string       # May be empty
  "region": string    # May be empty
}
```

## API

```python
def parse(url: string) -> dict
```

Primary export, parses input and returns documented dictionary.


## Examples

```python
from s3_endpoint_parse import parse

# All below:  s3["match"] is True
s3 = parse("https://s3.amazonaws.com/my-bucket/my/cool/file.png")

assert s3["protocol"] == "https"
assert s3["bucket"] == "my-bucket"
assert s3["region"] == "us-east-1"
assert s3["key"] == "my/cool/file.png"


s3 = parse("s3://my-bucket.s3.us-east-1.amazonaws.com.cn/my/cool/file.png")

assert s3["protocol"] == "s3"
assert s3["bucket"] == "my-bucket"
assert s3["region"] == "us-east-1"
assert s3["key"] == "my/cool/file.png"


s3 = parse("http://my-bucket.s3-us-east-1.amazonaws.com/my/cool/file.png")

assert s3["protocol"] == "http"
assert s3["bucket"] == "my-bucket"
assert s3["region"] == "us-east-1"
assert s3["key"] == "my/cool/file.png"


s3 = parse("https://my-bucket.s3-fips.dualstack.us-east-1.amazonaws.com/my/cool/file.png")

assert s3["protocol"] == "https"
assert s3["bucket"] == "my-bucket"
assert s3["region"] == "us-east-1"
assert s3["key"] == "my/cool/file.png"
```

See many more examples in the [`/tests/`](https://github.com/pckilgore/s3_endpoint_parse/blob/trunk/tests/test_s3_parse_url.py) folder
