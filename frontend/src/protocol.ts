export interface DictionaryStatus {
  statusMessage: string | null;
  pipelineMessage: string | null;
  errorInPreviousPipeline: string | null;
}

export type DictionaryStatusListener = (
  backendStatus: DictionaryStatus
) => void;

export interface CommandResponse {
  exception: string | null;
  headers: string[] | null;
  rows: any[][] | null;
}

export type CommandResponseListener = (
  commandResponse: CommandResponse
) => void;
