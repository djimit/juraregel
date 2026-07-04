// JuraRegel SDK — Main entry point

export { JuraregelClient } from "./client.js";
export * from "./types.js";

// Domain-specific clients
export { GriffierechtClient } from "./griffierecht.js";
export { Bio2Client } from "./bio2.js";
export { ForumStandaardisatieClient } from "./forumstandaardisatie.js";
export { OverheidsstandaardenClient } from "./overheidsstandaarden.js";
export { NoraClient } from "./nora.js";
export { EuAiActClient } from "./eu-ai-act.js";
export { AvgGdprClient } from "./avg-gdpr.js";
