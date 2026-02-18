import { useParams } from "react-router-dom";
import { useState } from "react";
import "../../../App.css";

const UserDetails = () => {
  const { userId } = useParams();
  const [activeTab, setActiveTab] = useState("personal");

  const renderTabContent = () => {
    switch (activeTab) {
      case "personal":
        return <div>Personal details for user {userId}</div>;
      case "payslips":
        return <div>Payslips data</div>;
      case "requests":
        return <div>Leave/WFH requests</div>;
      case "projects":
        return <div>Assigned projects</div>;
      case "progress":
        return <div>Task progress</div>;
      default:
        return null;
    }
  };

  return (
    <div>
      <h2>User Details (ID: {userId})</h2>

      <div className="tab-container">
        <button onClick={() => setActiveTab("personal")}>Personal</button>
        <button onClick={() => setActiveTab("payslips")}>Payslips</button>
        <button onClick={() => setActiveTab("requests")}>Requests</button>
        <button onClick={() => setActiveTab("projects")}>Projects</button>
        <button onClick={() => setActiveTab("progress")}>Progress</button>
      </div>

      <div className="tab-content">
        {renderTabContent()}
      </div>
    </div>
  );
};

export default UserDetails;