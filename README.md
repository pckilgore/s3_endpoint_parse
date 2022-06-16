# s3-endpoint-parse

Flexibly parses S3 URL/URIs, including legacy formats and new fips / dualstack
formats.

Returns a dict:
```
{
  "match": bool       # True if library matched
  "protocol": string  # May be empty
  "bucket": string    # Set if match is True
  "key": string       # May be empty
  "region": string    # May be empty
}
```

See /tests for examples.
