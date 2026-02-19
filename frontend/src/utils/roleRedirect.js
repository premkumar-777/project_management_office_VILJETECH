// src/utils/roleRedirect.js

export const getDashboardRoute = (role) => {
  switch (role) {
    case "super admin":
      return "/super-admin/dashboard";

    case "admin":
      return "/admin/dashboard";

    case "project manager":
      return "/project-manager/dashboard";

    case "employee":
      return "/employee/dashboard";

    case "client":
      return "/client/dashboard";

    default:
      return "/";
  }
};