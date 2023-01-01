import {Alert, Box} from '@dagster-io/ui';
import * as React from 'react';

import {DaemonHealthFragment} from '../instance/types/DaemonHealthFragment';

type Props = React.ComponentPropsWithRef<typeof Box> & {
  daemonHealth: DaemonHealthFragment | undefined;
};

export const SensorInfo: React.FC<Props> = ({daemonHealth, ...boxProps}) => {
  let healthy = undefined;

  if (daemonHealth) {
    const sensorHealths = daemonHealth.allDaemonStatuses.filter(
      (daemon) => daemon.daemonType === 'SENSOR',
    );
    if (sensorHealths) {
      const sensorHealth = sensorHealths[0];
      healthy = !!(sensorHealth.required && sensorHealth.healthy);
    }
  }

  if (healthy === false) {
    return (
      <Box {...boxProps}>
        <Alert
          intent="warning"
          title="The sensor daemon is not running."
          description={
            <div>
              See the{' '}
              <a
                href="https://ciusji.gitbook.io/sheenflow/deployment/main-concepts/sheenflow-daemon"
                target="_blank"
                rel="noreferrer"
              >
                sheenflow-daemon documentation
              </a>{' '}
              for more information on how to deploy the sheenflow-daemon process.
            </div>
          }
        />
      </Box>
    );
  }

  return null;
};
