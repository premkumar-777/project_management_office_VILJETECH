import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import AuthRoutes from "./pages/auth/AuthRoutes";
import DashboardRouter from "./pages/dashboard/DashboardRouter";

function App() {
  return (
    <Router>
      <Routes>
        {/* Auth routes */}
        <Route path="/*" element={<AuthRoutes />} />

        {/* Dashboard */}
        <Route path="/dashboard" element={<DashboardRouter />} />
      </Routes>
    </Router>
  );
}

export default App;
