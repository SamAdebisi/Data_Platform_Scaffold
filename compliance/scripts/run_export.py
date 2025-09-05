from __future__ import annotations
import os, csv, tempfile, pathlib
import duckdb
import pgpy
import paramiko

SQL_PATH = os.path.join(os.path.dirname(__file__), "..", "sql", "export_transactions.sql")
PUBLIC_KEY_PATH = os.path.join(os.path.dirname(__file__), "..", "pgp", "public.key")

S3_EP = os.getenv("S3_ENDPOINT", "http://minio:9000")
AWS_KEY = os.getenv("AWS_ACCESS_KEY_ID", "minio")
AWS_SEC = os.getenv("AWS_SECRET_ACCESS_KEY", "minio123")

SFTP_HOST = os.getenv("SFTP_HOST", "")
SFTP_PORT = int(os.getenv("SFTP_PORT", "22"))
SFTP_USER = os.getenv("SFTP_USER", "")
SFTP_PASS = os.getenv("SFTP_PASS", "")
SFTP_PATH = os.getenv("SFTP_PATH", "/upload/export.csv.pgp")


def _duckdb_conn():
    con = duckdb.connect()
    con.execute("INSTALL httpfs; LOAD httpfs;")
    con.execute(
        f"SET s3_endpoint='{S3_EP.replace('http://','').replace('https://','')}';"
    )
    con.execute("SET s3_url_style='path'; SET s3_use_ssl=false;")
    con.execute(f"SET s3_access_key_id='{AWS_KEY}'; SET s3_secret_access_key='{AWS_SEC}';")
    return con


def _pgp_encrypt(inp: bytes) -> bytes:
    # Why: PGP envelope to meet CSV-in-transit compliance
    if not os.path.exists(PUBLIC_KEY_PATH):
        raise RuntimeError("missing PGP public key")
    key, _ = pgpy.PGPKey.from_file(PUBLIC_KEY_PATH)
    msg = pgpy.PGPMessage.new(inp)
    enc = key.encrypt(msg)
    return bytes(enc)


def _sftp_put(data: bytes):
    if not SFTP_HOST:
        return  # optional in local runs
    transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
    transport.connect(username=SFTP_USER, password=SFTP_PASS)
    sftp = paramiko.SFTPClient.from_transport(transport)
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.write(data)
    tmp.flush()
    tmp.close()
    sftp.put(tmp.name, SFTP_PATH)
    sftp.close()
    transport.close()
    os.unlink(tmp.name)


def main():
    con = _duckdb_conn()
    sql = open(SQL_PATH, "r", encoding="utf-8").read()
    df = con.execute(sql).fetchdf()
    tmp_csv = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    df.to_csv(tmp_csv.name, index=False)
    with open(tmp_csv.name, "rb") as f:
        enc = _pgp_encrypt(f.read())
    _sftp_put(enc)
    print({"rows": len(df), "delivered": bool(SFTP_HOST)})


if __name__ == "__main__":
    main()
