from re import compile

"""
Virtual Hosted Style

http://BUCKET.s3.REGION.amazonaws.com/KEY
"""
virtual_hosted_style = compile(
    r"^([^:]+)(?:://)([^.]+)\.s3(?:-fips|\.dualstack|-fips\.dualstack)?\.([^.]+)\.amazonaws\.com(?:\.cn)?/?(.*?)$"
)

"""
Path Style

http://s3.REGION.amazonaws.com/BUCKET/KEY
"""
path_style = compile(
    r"^([^:]+)(?:://)s3(?:-fips|\.dualstack|-fips\.dualstack)?\.([^.]+)\.amazonaws\.com(?:\.cn)?/([^/]+)/?(.*?)$"
)

"""
Legacy Style Global Endpoint

http://BUCKET.s3.amazonaws.com/KEY
"""
legacy_global_endpoint = compile(r"^([^:]+)(?:://)([^.]+)\.s3\.amazonaws\.com/?(.*?)$")

"""
Legacy Style Global Endpoint With Path

http://s3.amazonaws.com/BUCKET/KEY
"""
legacy_global_endpoint_with_path = compile(
    r"^([^:]+)(?:://)s3\.amazonaws\.com?/([^/]+)/?(.*?)$"
)

"""
Legacy s3-region Style

https://BUCKET.s3-REGION.amazonaws.com/KEY
"""
legacy_s3region_style = compile(
    r"^([^:]+)(?:://)([^.]+)\.s3-([^.]+)\.amazonaws\.com/?(.*?)$"
)


def parse(url):
    """
    Parse the varying S3 URL forms into their parts into a dictionary:

    ```
    {
        "match": bool,
        "protocol": string,
        "bucket": string,
        "key": string,
        "region": string
    }
    ```

    "match" key is False if unable to parse the input string

    For example:

        - s3://my-bucket.s3-fips.us-east-1.amazonaws.com/path/to/obj
        - http://s3.amazonaws.com/my-bucket/path/to/obj
        - https://s3.us-east-1.amazonaws.com/my-bucket/path/to/obj

    See generally:

    https://docs.aws.amazon.com/AmazonS3/latest/userguide/VirtualHosting.html
    """

    result = {
        "match": False,
        "protocol": "",
        "bucket": "",
        "key": "",
        "region": "",
    }

    match = virtual_hosted_style.match(url)
    if match is not None:
        result["match"] = True
        result["protocol"] = match.group(1)
        result["bucket"] = match.group(2)
        result["key"] = match.group(4)
        result["region"] = match.group(3)

    match = path_style.match(url)
    if match is not None:
        result["match"] = True
        result["protocol"] = match.group(1)
        result["bucket"] = match.group(3)
        result["key"] = match.group(4)
        result["region"] = match.group(2)

    match = legacy_global_endpoint.match(url)
    if match is not None:
        result["match"] = True
        result["protocol"] = match.group(1)
        result["bucket"] = match.group(2)
        result["key"] = match.group(3)

    match = legacy_global_endpoint_with_path.match(url)
    if match is not None:
        result["match"] = True
        result["protocol"] = match.group(1)
        result["bucket"] = match.group(2)
        result["key"] = match.group(3)
        # Technically, this region is either US-EAST-1, or else it is invalid
        # since validation of that kind is out of scope, and this is a serious
        # edge case err on safety and leave region blank.

    match = legacy_s3region_style.match(url)
    if match is not None:
        result["match"] = True
        result["protocol"] = match.group(1)
        result["bucket"] = match.group(2)
        result["key"] = match.group(4)
        result["region"] = match.group(3)

    return result
