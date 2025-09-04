import os, csv, io, json, boto3
from .signer import sign_and_encrypt
from .sftp_client import sftp_put
def fetch_gold_sample():
    # placeholder. normally query warehouse.
    return [{"customer_id":"c1","txn_count":3,"total_amount":12.34,"last_ts":1}]
def run(kind: str):
    rows = fetch_gold_sample()
    buf=io.StringIO(); w=csv.DictWriter(buf, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    armored = os.getenv("PGP_PUBLIC_KEY","-----BEGIN PGP PUBLIC KEY BLOCK-----\n...\n-----END PGP PUBLIC KEY BLOCK-----")
    enc = sign_and_encrypt(buf.getvalue().encode(), armored)
    sftp_put(os.getenv("SFTP_HOST","localhost"), int(os.getenv("SFTP_PORT","22")), os.getenv("SFTP_USER","user"), os.getenv("SFTP_PASS","pass"), enc, f"/upload/{kind}.gpg")
if __name__=="__main__":
    import sys; run(sys.argv[1] if len(sys.argv)>1 else "daily")
