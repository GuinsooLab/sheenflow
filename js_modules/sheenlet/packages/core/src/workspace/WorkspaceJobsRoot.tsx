import {useQuery} from '@apollo/client';
import {Box, Colors, NonIdealState, Spinner, TextInput} from '@sheenflow-io/ui';
import * as React from 'react';

import {FIFTEEN_SECONDS, useQueryRefreshAtInterval} from '../app/QueryRefresh';
import {useTrackPageView} from '../app/analytics';
import {isHiddenAssetGroupJob} from '../asset-graph/Utils';
import {graphql} from '../graphql';

import {VirtualizedJobTable} from './VirtualizedJobTable';
import {WorkspaceHeader} from './WorkspaceHeader';
import {repoAddressAsHumanString} from './repoAddressAsString';
import {repoAddressToSelector} from './repoAddressToSelector';
import {RepoAddress} from './types';

export const WorkspaceJobsRoot = ({repoAddress}: {repoAddress: RepoAddress}) => {
  useTrackPageView();

  const [searchValue, setSearchValue] = React.useState('');

  const selector = repoAddressToSelector(repoAddress);

  const queryResultOverview = useQuery(WORKSPACE_JOBS_QUERY, {
    fetchPolicy: 'network-only',
    notifyOnNetworkStatusChange: true,
    variables: {selector},
  });
  const {data, loading} = queryResultOverview;
  const refreshState = useQueryRefreshAtInterval(queryResultOverview, FIFTEEN_SECONDS);

  const sanitizedSearch = searchValue.trim().toLocaleLowerCase();
  const anySearch = sanitizedSearch.length > 0;

  const jobs = React.useMemo(() => {
    if (data?.repositoryOrError.__typename === 'Repository') {
      return data.repositoryOrError.pipelines;
    }
    return [];
  }, [data]);

  const filteredBySearch = React.useMemo(() => {
    const searchToLower = sanitizedSearch.toLocaleLowerCase();
    return jobs.filter(
      ({name}) => !isHiddenAssetGroupJob(name) && name.toLocaleLowerCase().includes(searchToLower),
    );
  }, [jobs, sanitizedSearch]);

  const content = () => {
    if (loading && !data) {
      return (
        <Box flex={{direction: 'row', justifyContent: 'center'}} style={{paddingTop: '100px'}}>
          <Box flex={{direction: 'row', alignItems: 'center', gap: 16}}>
            <Spinner purpose="body-text" />
            <div style={{color: Colors.Gray600}}>Loading jobs…</div>
          </Box>
        </Box>
      );
    }

    const repoName = repoAddressAsHumanString(repoAddress);

    if (!filteredBySearch.length) {
      if (anySearch) {
        return (
          <Box padding={{top: 20}}>
            <NonIdealState
              icon="search"
              title="No matching jobs"
              description={
                <div>
                  No jobs matching <strong>{searchValue}</strong> were found in {repoName}
                </div>
              }
            />
          </Box>
        );
      }

      return (
        <Box padding={{top: 20}}>
          <NonIdealState
            icon="search"
            title="No jobs"
            description={`No jobs were found in ${repoName}`}
          />
        </Box>
      );
    }

    return <VirtualizedJobTable repoAddress={repoAddress} jobs={filteredBySearch} />;
  };

  return (
    <Box flex={{direction: 'column'}} style={{height: '100%', overflow: 'hidden'}}>
      <WorkspaceHeader
        repoAddress={repoAddress}
        tab="jobs"
        refreshState={refreshState}
        queryData={queryResultOverview}
      />
      <Box padding={{horizontal: 24, vertical: 16}}>
        <TextInput
          icon="search"
          value={searchValue}
          onChange={(e) => setSearchValue(e.target.value)}
          placeholder="Filter by job name…"
          style={{width: '340px'}}
        />
      </Box>
      {loading && !data ? (
        <Box padding={64}>
          <Spinner purpose="page" />
        </Box>
      ) : (
        content()
      )}
    </Box>
  );
};

export const WORKSPACE_JOBS_QUERY = graphql(`
  query WorkspaceJobsQuery($selector: RepositorySelector!) {
    repositoryOrError(repositorySelector: $selector) {
      ... on Repository {
        id
        name
        pipelines {
          id
          name
          isJob
        }
      }
      ...PythonErrorFragment
    }
  }
`);