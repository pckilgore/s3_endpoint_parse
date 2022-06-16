from s3_parse_url import parse

bucket = "my-bucket"
key = "path/to/object"
region = "xyz-to-nowhere"

def test_invalid_empty():
    result = parse("")
    assert result["match"] is False


def test_invalid_random():
    result = parse("http://www.google.com/bucket/path")
    assert result["match"] is False


def test_invalid_proto():
    result = parse("//s3.amazonaws.com/bucket/key")
    assert result["match"] is False


def virtual_hosted_style():
    host = f"{bucket}.s3.{region}.amazonaws.com"
    host_fips = f"{bucket}.s3-fips.{region}.amazonaws.com"
    host_dual = f"{bucket}.s3.dualstack.{region}.amazonaws.com"
    host_both = f"{bucket}.s3-fips.dualstack.{region}.amazonaws.com"

    fixtures = [
        # (url, path, region)
        (f"https://{host}/{key}", key, region),
        (f"http://{host}/", '', region),
        (f"s3://{host}", '', region),
        (f"https://{host_fips}/{key}", key, region),
        (f"http://{host_fips}/", '', region),
        (f"s3://{host_fips}", '', region),
        (f"https://{host_dual}/{key}", key, region),
        (f"http://{host_dual}/", '', region),
        (f"s3://{host_dual}", '', region),
        (f"https://{host_both}/{key}", key, region),
        (f"http://{host_both}/", '', region),
        (f"s3://{host_both}", '', region),
    ]


def test_path_style():
    host = f"s3.{region}.amazonaws.com"
    host_fips = f"s3-fips.{region}.amazonaws.com"
    host_dual = f"s3.dualstack.{region}.amazonaws.com"
    host_both = f"s3-fips.dualstack.{region}.amazonaws.com"

    fixtures = [
        # (url, path, region)
        (f"https://{host}/{bucket}/{key}", key, region),
        (f"http://{host}/{bucket}/", '', region),
        (f"s3://{host}/{bucket}", '', region),
        (f"s3://{host_fips}/{bucket}/{key}", key, region),
        (f"https://{host_fips}/{bucket}/", '', region),
        (f"http://{host_fips}/{bucket}", '', region),
        (f"https://{host_dual}/{bucket}/{key}", key, region),
        (f"s3://{host_dual}/{bucket}/", '', region),
        (f"http://{host_dual}/{bucket}", '', region),
        (f"https://{host_both}/{bucket}/{key}", key, region),
        (f"https://{host_both}/{bucket}/", '', region),
        (f"s3://{host_both}/{bucket}", '', region),
    ]

    for (url, want_key, want_region) in fixtures:
        got = parse(url)
        assert got["match"] is True
        assert got["bucket"] == bucket
        assert got["key"] == want_key
        assert got["region"] == want_region


def test_path_style_no_match_no_bucket():
    host = f"s3.{region}.amazonaws.com"

    fixtures = [
        # (url, path, region)
        (f"http://{host}/", '', region),
        (f"s3://{host}", '', region),
    ]

    for (url, _, _) in fixtures:
        got = parse(url)
        assert got["match"] is False


def test_legacy_global_endpoint():
    host = f"{bucket}.s3.amazonaws.com"
    fixtures = [
        # (url, path, region)
        (f"https://{host}/{key}", key, ''),
        (f"http://{host}/", '', ''),
        (f"s3://{host}", '', ''),
    ]

    for (url, want_key, want_region) in fixtures:
        got = parse(url)
        assert got["match"] is True
        assert got["bucket"] == bucket
        assert got["key"] == want_key
        assert got["region"] == want_region


def test_legacy_global_endpoint():
    host = f"{bucket}.s3.amazonaws.com"
    fixtures = [
        # (url, path, region)
        (f"https://{host}/{key}", key, ''),
        (f"http://{host}/", '', ''),
        (f"s3://{host}", '', ''),
    ]

    for (url, want_key, want_region) in fixtures:
        got = parse(url)
        assert got["match"] is True
        assert got["bucket"] == bucket
        assert got["key"] == want_key
        assert got["region"] == want_region


def test_legacy_global_endpoint_us_east():
    host = "s3.amazonaws.com"
    fixtures = [
        # (url, path, region)
        (f"http://{host}/{bucket}/{key}", key, ''),
        (f"s3://{host}/{bucket}", '', ''),
        (f"https://{host}/{bucket}/", '', ''),
    ]

    for (url, want_key, want_region) in fixtures:
        got = parse(url)
        assert got["match"] is True
        assert got["bucket"] == bucket
        assert got["key"] == want_key
        assert got["region"] == want_region


def test_legacy_s3_region():
    host = f"{bucket}.s3-{region}.amazonaws.com"

    fixtures = [
        # (url, region)
        (f"https://{host}/{key}", key, region),
        (f"s3://{host}/", "", region),
        (f"http://{host}", "", region),
    ]

    for (url, want_key, want_region) in fixtures:
        got = parse(url)
        assert got["match"] is True
        assert got["bucket"] == bucket
        assert got["key"] == want_key
        assert got["region"] == want_region


def test_protocol_parse():
    endpoint = f"{bucket}.s3.{region}.amazonaws.com/{bucket}/{key}"

    fixtures = [
        # (url, proto)
        (f"https://{endpoint}", "https"),
        (f"http://{endpoint}", "http"),
        (f"s3://{endpoint}", "s3"),
        (f"my-s3-protocol://{endpoint}", "my-s3-protocol"),
        (f"://{endpoint}", ""),
        (endpoint, ""),

    ]

    for (url, want_proto) in fixtures:
        got = parse(url)
        assert got["protocol"] == want_proto

