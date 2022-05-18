import React from "react";
import ReactDOM from "react-dom/client";
import { App } from "./App";

function getBackendPort(): number {
  const queryParams = new URLSearchParams(window.location.search);
  const backendPort = queryParams.get("backend-port");

  return Number(backendPort ?? location.port);
}
const websocketPort = getBackendPort();

const rootElement = document.createElement("div");
document.body.append(rootElement);

ReactDOM.createRoot(rootElement).render(<App websocketPort={websocketPort} />);
