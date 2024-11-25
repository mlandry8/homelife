import datetime
import ipaddress

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import NameOID
from cryptography import x509


def generate_cert(ip: str | None = None) -> tuple[bytes, bytes]:
    private_key: rsa.RSAPrivateKey = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    public_key: rsa.RSAPublicKey = private_key.public_key()

    builder: x509.CertificateBuilder = x509.CertificateBuilder()
    builder = builder.subject_name(
        x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "homelife")])
    )
    builder = builder.issuer_name(
        x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "homelife")])
    )
    builder = builder.not_valid_before(
        datetime.datetime.today() - datetime.timedelta(1, 0, 0)
    )
    builder = builder.not_valid_after(
        datetime.datetime.today() + (datetime.timedelta(1, 0, 0) * 365 * 5)
    )
    builder = builder.serial_number(x509.random_serial_number())
    builder = builder.public_key(public_key)
    if ip:
        builder = builder.add_extension(
            x509.SubjectAlternativeName([x509.IPAddress(ipaddress.IPv4Address(ip))]),
            critical=False,
        )
    builder = builder.add_extension(
        x509.BasicConstraints(ca=False, path_length=None), critical=True
    )

    certificate: x509.Certificate = builder.sign(
        private_key=private_key, algorithm=hashes.SHA256(), backend=default_backend()
    )

    return (
        certificate.public_bytes(serialization.Encoding.PEM),
        private_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        ),
    )


def get_certificate_fingerprint(cert_pem: bytes) -> str:
    cert: x509.Certificate = x509.load_pem_x509_certificate(cert_pem, default_backend())
    fingerprint: bytes = cert.fingerprint(hashes.SHA256())
    return fingerprint.hex()


def verify_certificate_fingerprint(cert_pem: bytes, expected_fingerprint: str) -> bool:
    fingerprint: str = get_certificate_fingerprint(cert_pem)
    return fingerprint == expected_fingerprint
