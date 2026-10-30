// Shared data-access layer for the dashboard. Screens call getDashboard() and never
// import fixtures directly, so the mock API (#12) or real API can replace this later.
import normal from "./fixtures/dashboard-normal.json";
import empty from "./fixtures/dashboard-empty.json";
import deviceDisconnected from "./fixtures/dashboard-device-disconnected.json";
import error from "./fixtures/dashboard-error.json";
 
export type DashboardScenario = "normal" | "empty" | "device-disconnected" | "error";
 
const fixtures = {
  normal,
  empty,
  "device-disconnected": deviceDisconnected,
  error,
};
 
export class DashboardRequestError extends Error {
  constructor(
    public code: string,
    public retryable: boolean,
  ) {
    super(code);
  }
}
 
export async function getDashboard(scenario: DashboardScenario = "normal") {
  const response = fixtures[scenario];
  if ("error" in response) {
    throw new DashboardRequestError(response.error.code, response.error.retryable);
  }
  return response;
}