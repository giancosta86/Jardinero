import React from "react";
import { CommandResponse } from "../../protocol";
import styles from "./OutputBox.module.scss";

interface Props {
  commandResponse: CommandResponse;
}

export const OutputBox = ({ commandResponse }: Props) => {
  return (
    <div className={styles.outputBox}>
      {commandResponse.exception && (
        <div className={styles.errorBox}>{commandResponse.exception}</div>
      )}

      {commandResponse.headers && commandResponse.rows && (
        <>
          <div className={styles.countBox}>
            <label>Total rows: </label> {commandResponse.rows.length}
          </div>

          <table>
            <thead>
              {commandResponse.headers.map(header => (
                <td>{header}</td>
              ))}
            </thead>
            <tbody>
              {commandResponse.rows.map(row => (
                <tr>
                  {row.map(cell => (
                    <td>{cell}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
    </div>
  );
};
