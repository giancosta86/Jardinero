import React from "react";
import spinner from "../spinner.svg";
import styles from "./PipelineBox.module.scss";

interface Props {
  pipelineMessage: string | null;
  hasDictionary: boolean;
  startPipeline: () => void;
  cancelPipeline: () => void;
}

const REPLACE_DICTIONARY_PROMPT =
  "A dictionary was already created by Jardinero for this language module: " +
  "if you start the pipeline now, the existing copy will be replaced " +
  "at the end of the process.\n" +
  "\n" +
  "However, you will still be able to run queries on the current dictionary " +
  "in the meantime.\n" +
  "\n" +
  "Do you want to continue?";

export const PipelineBox = ({
  pipelineMessage,
  hasDictionary,
  startPipeline,
  cancelPipeline
}: Props) => {
  const isPipelineRunning = pipelineMessage != null;

  const handleStartPipelineClick = () => {
    if (hasDictionary && !confirm(REPLACE_DICTIONARY_PROMPT)) {
      return;
    }
    startPipeline();
  };

  const handleCancelPipelineClick = () => {
    if (!confirm("Are you sure you want to cancel?")) {
      return;
    }

    cancelPipeline();
  };

  const startButtonLabel = hasDictionary
    ? "Update dictionary"
    : "Create dictionary";

  return (
    <div className={styles.pipelineBox}>
      {isPipelineRunning && (
        <>
          <img className={styles.spinner} src={spinner} />
          <div>
            <label>{pipelineMessage}</label>
          </div>
          <button
            className={styles.cancelButton}
            onClick={handleCancelPipelineClick}
          >
            Cancel pipeline
          </button>
        </>
      )}

      {!isPipelineRunning && (
        <button
          className={styles.startButton}
          onClick={handleStartPipelineClick}
        >
          {startButtonLabel}
        </button>
      )}
    </div>
  );
};
