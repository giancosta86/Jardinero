import React, { useState } from "react";
import { CommandBox } from "./components/Command/InputBox";
import { OutputBox } from "./components/Command/OutputBox";
import { DictionaryBox } from "./components/DictionaryBox";
import { useBackendWebSocket } from "./hooks/useBackendWebSocket";
import { useCommandState } from "./hooks/useCommandState";
import logo from "./logo.svg";
import { DictionaryStatus } from "./protocol";
import "./styles/globals.scss";

interface Props {
  websocketPort: number;
}

export const App = ({ websocketPort }: Props) => {
  const [dictionaryStatus, setDictionaryStatus] = useState<DictionaryStatus>(
    () => ({
      statusMessage: null,
      pipelineMessage: null,
      errorInPreviousPipeline: null
    })
  );

  const {
    response: commandResponse,
    running: commandRunning,
    startRunning,
    responseListener: commandResponseListener
  } = useCommandState();

  const dictionaryControl = useBackendWebSocket(
    websocketPort,
    setDictionaryStatus,
    commandResponseListener
  );

  const hasDictionary = dictionaryStatus.statusMessage != null;

  const runCommand = (command: string) => {
    startRunning();
    dictionaryControl.runCommand(command);
  };

  return (
    <div className="main">
      <header>
        <img className="logo" src={logo}></img>
      </header>

      {hasDictionary && (
        <CommandBox runCommand={runCommand} commandRunning={commandRunning} />
      )}

      <OutputBox commandResponse={commandResponse} />

      <DictionaryBox
        dictionaryStatus={dictionaryStatus}
        startPipeline={dictionaryControl.startPipeline}
        cancelPipeline={dictionaryControl.cancelPipeline}
      />

      <footer>
        Created by <a href="https://gianlucacosta.info/">Gianluca Costa</a>{" "}
        using <a href="https://github.com/giancosta86/Eos-core">Eos-core</a> and{" "}
        <a href="https://github.com/giancosta86/WikiPrism">WikiPrism</a>{" "}
      </footer>
    </div>
  );
};
