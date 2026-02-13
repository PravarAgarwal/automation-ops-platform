export type ScriptType = "python";

export interface Job {
    id: string;
    name: string;
    script_type: ScriptType;
    script_content: string;

}