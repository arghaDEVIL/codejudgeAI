import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./Login";
import Register from "./Register";
import Judge from "./Judge";
import Dashboard from "./pages/Dashboard";
import AdminPanel from "./pages/AdminPanel";
import SubmissionHistory from "./SubmissionHistory";
import SubmissionDetail from "./SubmissionDetail";
import RoomLobby from "./pages/RoomLobby";
import CollaborativeRoom from "./pages/CollaborativeRoom";
import { isAuthenticated } from "./utils/api";
import { ThemeProvider } from "./components/theme-provider";

function App() {
  const isAuth = isAuthenticated();

  return (
    <ThemeProvider defaultTheme="dark" storageKey="ui-theme">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Navigate to={isAuth ? "/dashboard" : "/login"} />} />
          <Route path="/login" element={isAuth ? <Navigate to="/dashboard" /> : <Login />} />
          <Route path="/signup" element={isAuth ? <Navigate to="/dashboard" /> : <Register />} />
          <Route path="/register" element={<Navigate to="/signup" />} />
          <Route path="/dashboard" element={isAuth ? <Dashboard /> : <Navigate to="/login" />} />
          <Route path="/judge" element={isAuth ? <Judge /> : <Navigate to="/login" />} />
          <Route path="/admin" element={isAuth ? <AdminPanel /> : <Navigate to="/login" />} />
          <Route path="/history" element={isAuth ? <SubmissionHistory /> : <Navigate to="/login" />} />
          <Route path="/submission/:id" element={isAuth ? <SubmissionDetail /> : <Navigate to="/login" />} />
          <Route path="/rooms" element={isAuth ? <RoomLobby /> : <Navigate to="/login" />} />
          <Route path="/room/:roomCode" element={isAuth ? <CollaborativeRoom /> : <Navigate to="/login" />} />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;