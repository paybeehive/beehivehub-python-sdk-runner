import json

from src.utils import (
    format_currency,
    load_payload,
    print_error,
    print_result,
    print_result_with_file,
    print_success,
    save_output,
)


def test_format_currency_basic():
    assert format_currency(10000) == "R$ 100,00"


def test_format_currency_cents():
    assert format_currency(1) == "R$ 0,01"


def test_format_currency_thousands():
    assert format_currency(1000000) == "R$ 10.000,00"


def test_format_currency_zero():
    assert format_currency(0) == "R$ 0,00"


def test_load_payload_valid():
    payload = load_payload("customer-create.json")
    assert isinstance(payload, dict)
    assert "name" in payload
    assert "email" in payload


def test_load_payload_not_found():
    try:
        load_payload("nonexistent.json")
        assert False, "Should have raised FileNotFoundError"
    except FileNotFoundError:
        pass


def test_save_output(tmp_path, monkeypatch):
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))

    data = {"id": 1, "status": "paid"}
    filepath = save_output("test_operation", data)

    assert "test_operation" in filepath
    with open(filepath, encoding="utf-8") as f:
        saved = json.load(f)
    assert saved["operation"] == "test_operation"
    assert saved["data"] == data


def test_save_output_with_sdk_info(tmp_path, monkeypatch):
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))

    data = {"id": 1}
    sdk_info = {"environment": "sandbox"}
    filepath = save_output("test_op", data, sdk_info)

    with open(filepath, encoding="utf-8") as f:
        saved = json.load(f)
    assert saved["sdk_info"] == sdk_info


def test_print_success(capsys):
    print_success("operation completed")
    output = capsys.readouterr().out
    assert "✓" in output
    assert "operation completed" in output


def test_print_error(capsys):
    print_error("something failed")
    output = capsys.readouterr().out
    assert "✗" in output
    assert "something failed" in output


def test_print_result_with_list(capsys):
    print_result([1, 2, 3])
    output = capsys.readouterr().out
    assert "Items returned: 3" in output


def test_print_result_with_dict(capsys):
    print_result({"a": 1, "b": 2})
    output = capsys.readouterr().out
    assert "Keys: 2" in output


def test_print_result_with_file_saves_and_prints(capsys, tmp_path, monkeypatch):
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))

    data = {"id": 42, "status": "paid"}
    print_result_with_file("test_op", data)
    output = capsys.readouterr().out

    assert "Keys: 2" in output
    assert "Output saved to:" in output

    files = list(tmp_path.glob("*.json"))
    assert len(files) == 1


def test_format_currency_negative():
    # Negative amounts are formatted as-is — no special handling, documents current behavior
    result = format_currency(-100)
    assert "R$" in result
    assert "-" in result


def test_print_result_with_non_collection(capsys):
    # When data is neither list nor dict, no summary line is printed — just the JSON value
    print_result("raw string value")
    output = capsys.readouterr().out
    assert "raw string value" in output
    assert "Items returned" not in output
    assert "Keys:" not in output


def test_load_payload_returns_dict_with_expected_structure():
    # Validates that all required customer payload fields are present
    payload = load_payload("customer-create.json")
    assert isinstance(payload, dict)
    assert len(payload) > 0


def test_save_output_filename_contains_operation(tmp_path, monkeypatch):
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))
    filepath = save_output("my_operation", {"key": "value"})
    assert "my_operation" in filepath


def test_save_output_timestamp_is_in_utc_format(tmp_path, monkeypatch):
    import json

    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))
    filepath = save_output("check_timestamp", {})
    with open(filepath, encoding="utf-8") as f:
        saved = json.load(f)
    # Timestamp should follow ISO format YYYY-MM-DDTHH-MM-SS
    ts = saved["timestamp"]
    assert len(ts) == 19
    assert ts[4] == "-" and ts[7] == "-" and ts[10] == "T"
