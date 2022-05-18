import React from "react";
import spinner from "../spinner.svg";
import styles from "./RunButton.module.scss";

interface Props {
  commandRunning: boolean;
  onClick: () => void;
}

export const RunButton = ({ commandRunning, onClick }: Props) => (
  <button
    className={styles.runButton}
    onClick={onClick}
    disabled={commandRunning}
  >
    <div>
      {commandRunning && <img className={styles.runSpinner} src={spinner} />}
      <span>{commandRunning ? "Running..." : "Run"}</span>
    </div>
  </button>
);
