import convertRelayPiiConfig from 'app/views/settings/components/dataScrubbing/convertRelayPiiConfig';

// @ts-ignore
const relayPiiConfig = TestStubs.DataScrubbingRelayPiiConfig();
const stringRelayPiiConfig = JSON.stringify(relayPiiConfig);
const convertedRules = convertRelayPiiConfig(stringRelayPiiConfig);

export {convertedRules, stringRelayPiiConfig, relayPiiConfig};
