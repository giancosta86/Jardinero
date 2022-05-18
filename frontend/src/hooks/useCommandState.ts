import { useState } from "react";
import { CommandResponse, CommandResponseListener } from "../protocol";

interface CommandState {
  running: boolean;
  startRunning: () => void;
  response: CommandResponse;
  responseListener: CommandResponseListener;
}

export function useCommandState(): CommandState {
  const [running, setRunning] = useState(false);

  const [response, setResponse] = useState<CommandResponse>(() => ({
    exception: null,
    headers: null,
    rows: null
  }));

  const responseListener = (response: CommandResponse) => {
    setRunning(false);
    setResponse(response);
  };

  const startRunning = () => {
    setRunning(true);
  };

  return {
    running,
    startRunning,
    response,
    responseListener
  };
}
