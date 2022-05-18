import React from "react";
import styles from "./StatusBox.module.scss";

interface Props {
  statusMessage: string | null;
  errorInPreviousPipeline: string | null;
}

export const StatusBox = ({
  statusMessage,
  errorInPreviousPipeline
}: Props) => {
  return (
    <div className={styles.statusBox}>
      <div>
        <label>{statusMessage ?? "(dictionary not created yet)"}</label>
      </div>

      {errorInPreviousPipeline && (
        <div className={styles.errorInLatestPipeline}>
          <label>Latest error when trying to update the dictionary:</label>
          {errorInPreviousPipeline}
        </div>
      )}
    </div>
  );
};
