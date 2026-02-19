// src/pages/auth/MFASetupPage.jsx
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import QRCode from "qrcode";

export default function MFASetupPage() {
  const [qrUri, setQrUri] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const storedQrUri = sessionStorage.getItem("qr_uri");
    if (!storedQrUri) {
      alert("QR not found. Complete registration first.");
      return navigate("/registration");
    }
    setQrUri(storedQrUri);
  }, [navigate]);

  const handleNext = () => {
    navigate("/auth/mfa"); // go to OTP verification
  };

  return (
    <div className="mfa-setup-page">
      <h2>Scan this QR code with your Authenticator app</h2>
      {qrUri && <QRCode value={qrUri} size={250} />}
      <button onClick={handleNext}>Next</button>
    </div>
  );
}
