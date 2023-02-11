import {Box, Colors, Icon, IconWrapper, Tooltip} from '@dagster-io/ui';
import * as React from 'react';
import {Link, NavLink, useHistory} from 'react-router-dom';
import styled from 'styled-components/macro';

import {DeploymentStatusIcon} from '../nav/DeploymentStatusIcon';
import {VersionNumber} from '../nav/VersionNumber';
import {SearchDialog} from '../search/SearchDialog';

import {LayoutContext} from './LayoutProvider';
import {ShortcutHandler} from './ShortcutHandler';
import {WebSocketStatus} from './WebSocketProvider';
import menu_book from "@dagster-io/ui/icon-svgs/menu_book.svg";

type AppNavLinkType = {
  title: string;
  element: React.ReactNode;
};
interface Props {
  searchPlaceholder: string;
  rightOfSearchBar?: React.ReactNode;
  showStatusWarningIcon?: boolean;
  getNavLinks?: (navItems: AppNavLinkType[]) => React.ReactNode;
}

const unifiedBk = '#072C4F';

export const AppTopNav: React.FC<Props> = ({
  children,
  rightOfSearchBar,
  searchPlaceholder,
  getNavLinks,
}) => {
  const history = useHistory();

  const navLinks = () => {
      let absolute;
      return [
      {
        title: 'overview',
        element: (
          <ShortcutHandler
            key="overview"
            onShortcut={() => history.push('/overview')}
            shortcutLabel="⌥1"
            shortcutFilter={(e) => e.altKey && e.code === 'Digit1'}
          >
            <TopNavLink to="/overview" data-cy="AppTopNav_StatusLink">
              <Icon name="waterfall_chart" size={20} color={Colors.White} />
            </TopNavLink>
          </ShortcutHandler>
        ),
      },
      {
        title: 'runs',
        element: (
          <ShortcutHandler
            key="runs"
            onShortcut={() => history.push('/runs')}
            shortcutLabel="⌥2"
            shortcutFilter={(e) => e.altKey && e.code === 'Digit2'}
          >
            <TopNavLink to="/runs" data-cy="AppTopNav_RunsLink">
              <Icon name="job" size={20} color={Colors.White} />
            </TopNavLink>
          </ShortcutHandler>
        ),
      },
      {
        title: 'assets',
        element: (
          <ShortcutHandler
            key="assets"
            onShortcut={() => history.push('/assets')}
            shortcutLabel="⌥3"
            shortcutFilter={(e) => e.altKey && e.code === 'Digit3'}
          >
            <TopNavLink
              to="/assets"
              data-cy="AppTopNav_AssetsLink"
              isActive={(_, location) => {
                const {pathname} = location;
                return pathname.startsWith('/assets') || pathname.startsWith('/asset-groups');
              }}
              exact={false}
            >
              <Icon name="asset" size={20} color={Colors.White} />
            </TopNavLink>
          </ShortcutHandler>
        ),
      },
      {
        title: 'deployment',
        element: (
          <ShortcutHandler
            key="deployment"
            onShortcut={() => history.push('/locations')}
            shortcutLabel="⌥4"
            shortcutFilter={(e) => e.altKey && e.code === 'Digit4'}
          >
            <TopNavLink
              to="/locations"
              data-cy="AppTopNav_StatusLink"
              isActive={(_, location) => {
                const {pathname} = location;
                return (
                  pathname.startsWith('/locations') ||
                  pathname.startsWith('/health') ||
                  pathname.startsWith('/config')
                );
              }}
            >
              <Box flex={{direction: 'row', alignItems: 'center', gap: 6}}>
                <Icon name="tune" size={20} color={Colors.White} />
                <DeploymentStatusIcon />
              </Box>
            </TopNavLink>
          </ShortcutHandler>
        ),
      },
      {
        title: 'help',
        element: (
          <ShortcutHandler key="help">
            <div onClick={() => window.open('https://ciusji.gitbook.io/sheenflow/', '_target')}>
              <Icon
                name="menu_book"
                size={20}
                color={Colors.White}
                style={{position: 'absolute', bottom: 0, left: 0, margin: '20px'}}
              />
            </div>
          </ShortcutHandler>
        ),
      },
    ];
  };

  return (
    <AppTopNavContainer>
      <Box flex={{direction: 'row', alignItems: 'center', gap: 16}}>
        <AppTopNavLogo />
        <Box
          margin={{left: 0}}
          flex={{direction: 'column', alignItems: 'center'}}
          style={{
            backgroundColor: unifiedBk,
            width: 60,
            position: 'absolute',
            top: 0,
            left: 0,
            height: '100vh',
            zIndex: 500,
            paddingTop: 60,
          }}
        >
          {getNavLinks ? getNavLinks(navLinks()) : navLinks().map((link) => link.element)}
        </Box>
        {rightOfSearchBar}
      </Box>
      <Box flex={{direction: 'row', alignItems: 'center'}}>
        <SearchDialog searchPlaceholder={searchPlaceholder} />
        {children}
      </Box>
    </AppTopNavContainer>
  );
};

export const AppTopNavLogo: React.FC = () => {
  const {nav} = React.useContext(LayoutContext);
  const navButton = React.useRef<null | HTMLButtonElement>(null);

  const onToggle = React.useCallback(() => {
    navButton.current && navButton.current.focus();
    nav.isOpen ? nav.close() : nav.open();
  }, [nav]);

  const onKeyDown = React.useCallback(
    (e) => {
      if (e.key === 'Escape' && nav.isOpen) {
        nav.close();
      }
    },
    [nav],
  );

  return (
    <LogoContainer>
      {nav.canOpen ? (
        <ShortcutHandler
          onShortcut={() => onToggle()}
          shortcutLabel="."
          shortcutFilter={(e) => e.key === '.'}
        >
          <NavButton onClick={onToggle} onKeyDown={onKeyDown} ref={navButton}>
            <Icon name="menu" color={Colors.White} size={20} />
          </NavButton>
        </ShortcutHandler>
      ) : null}
      <Box flex={{display: 'inline-flex'}} margin={{left: 8}}>
        <DaggyTooltip
          content={
            <Box flex={{direction: 'row', gap: 4}}>
              <WebSocketStatus />
              <VersionNumber />
            </Box>
          }
          placement="bottom"
          modifiers={{offset: {enabled: true, options: {offset: [18, 0]}}}}
        >
          <Link
            to="/home"
            style={{
              outline: 0,
              display: 'flex',
              position: 'absolute',
              top: 0,
              left: 0,
              width: 60,
              height: 60,
              alignItems: 'center',
              justifyContent: 'center',
              zIndex: 700,
            }}
          >
            <GhostDaggy />
          </Link>
        </DaggyTooltip>
      </Box>
    </LogoContainer>
  );
};

const GhostDaggy = () => (
  <svg
    width="29px"
    height="29px"
    viewBox="0 0 29 29"
    version="1.1"
    xmlns="http://www.w3.org/2000/svg"
  >
    <title>sheenflow</title>
    <g id="Page-1" stroke="none" strokeWidth="1" fill="none" fillRule="evenodd">
      <g id="sheenflow" transform="translate(0.351876, 0.579708)" fillRule="nonzero">
        <path
          d="M0,10.0195069 C3.44573561,8.98044616 5.72100105,7.8617532 6.82579626,6.66342797 C7.93059149,5.46510276 8.73448555,3.24396009 9.23747842,-1.53271853e-15 L18.1996065,-1.53271853e-15 C17.849046,3.49757433 17.4610561,5.89228792 17.0356364,7.18414074 C16.0771633,10.0946935 14.4147981,11.9069141 13.1741552,13.165013 C11.9669404,14.3892135 10.1127193,15.9842784 7.31897458,16.9817976 C7.06051742,17.0740809 6.75974183,17.1670432 6.4166478,17.2606844 C5.47196818,17.5185175 3.33308558,17.9168485 0,18.4556776 L0,10.0195069 Z"
          id="Path-11"
          fill="#8323EF"
        />
        <polygon
          id="Path-12"
          fill="#33C89B"
          points="9.0998032 18.4556776 18.1996065 18.4556776 18.1996065 28 9.0998032 28"
        />
        <polygon
          id="Path-13"
          fill="#33C89B"
          points="19.2975673 10.3883221 19.2975673 28 28 28 28 10.3883221"
        />
      </g>
    </g>
  </svg>
);

const DaggyTooltip = styled(Tooltip)`
  &.bp3-popover2-target {
    display: inline-flex;
  }
`;

export const TopNavLink = styled(NavLink)`
  color: ${Colors.Gray400};
  font-weight: 600;
  transition: color 50ms linear;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;

  :hover a {
    background: ${Colors.Gray900};
    text-decoration: none;
  }

  :active,
  &.active {
    border-left: 4px solid ${Colors.Blue500};
    border-right: 4px solid ${unifiedBk};
    text-decoration: none;
  }

  :focus {
    outline: none !important;
    color: ${Colors.Blue500};
  }
`;

export const AppTopNavContainer = styled.div`
  // background: ${Colors.Gray900};
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  height: 47px;
  border-bottom: 1px solid #e9e8e8;
`;

const LogoContainer = styled.div`
  cursor: pointer;
  display: flex;
  align-items: center;
  flex-shrink: 0;
  padding-left: 12px;

  svg {
    transition: filter 100ms;
  }

  &:hover {
    svg {
      filter: brightness(90%);
    }
  }
`;

const NavButton = styled.button`
  border-radius: 20px;
  cursor: pointer;
  margin-left: 4px;
  outline: none;
  // padding: 6px;
  border: none;
  background: transparent;
  display: block;

  ${IconWrapper} {
    transition: background 100ms linear;
  }

  :hover ${IconWrapper} {
    background: ${Colors.Gray500};
  }

  :active ${IconWrapper} {
    background: ${Colors.Blue200};
  }

  :focus {
    background: ${Colors.Gray700};
  }
`;
