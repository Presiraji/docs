import React, { useState, useCallback } from "react";
import Head from "next/head";
import { useRouter } from "next/router";

import { getMenu } from "../lib/api";

import Layout from "../components/layouts/globalTemplate";
import Footer from "../components/navigation/footer";

import SideBar from "../components/navigation/sideBar";
import ArrowLinkContainer from "../components/navigation/arrowLinkContainer";
import ArrowLink from "../components/navigation/arrowLink";

import GDPRBanner, {
  setTelemetryPreference,
} from "../components/utilities/gdpr";
import CookieSettingsModal from "../components/utilities/cookieSettingsModal";
import SocialCallouts from "../components/utilities/socialCallout";
import Spacer from "../components/utilities/spacer";

import SummaryTiles from "../components/summaryTiles";

import NewsContainer from "../components/layouts/newsContainer";
import InlineCalloutContainer from "../components/layouts/inlineCalloutContainer";
import TileContainer from "../components/layouts/tileContainer";
import RefCard from "../components/blocks/refCard";

import { H1, H2 } from "../components/blocks/headers";
import NewsFeed from "../components/blocks/newsFeed";
import Button from "../components/blocks/button";
import InlineCallout from "../components/blocks/inlineCallout";
import NoteSplit from "../components/blocks/noteSplit";

import { attributes } from "../content/index.md";

import styles from "../components/layouts/container.module.css";

export default function Home({ window, menu }) {
  let { description } = attributes;

  const [isTelemetryModalVisible, setIsTelemetryModalVisible] = useState(false);
  const [isTelemetryBannerVisible, setIsTelemetryBannerVisible] =
    useState(false);
  const [insertTelemetryCode, setInsertTelemetryCode] = useState(false);

  const router = useRouter();

  const allowTelemetryAndCloseBanner = useCallback(() => {
    setIsTelemetryBannerVisible(false);
    setIsTelemetryModalVisible(false);
    setInsertTelemetryCode(true);
    setTelemetryPreference(true);
  }, [isTelemetryBannerVisible, insertTelemetryCode]);

  const declineTelemetryAndCloseBanner = useCallback(() => {
    setIsTelemetryBannerVisible(false);
    setIsTelemetryModalVisible(false);
    setInsertTelemetryCode(false);
    setTelemetryPreference(false);

    // If previous state was true, and now it's false, reload the page to remove telemetry JS
    if (insertTelemetryCode) router.reload();
  }, [isTelemetryBannerVisible, insertTelemetryCode]);

  return (
    <Layout window={window}>
      <Head>
        <title>Streamlit documentation</title>
        <link rel="icon" href="/favicon.svg" />
        <link rel="alternate icon" href="/favicon32.ico" />
        <meta name="theme-color" content="#ffffff" />
        <link
          rel="canonical"
          href={`https://${process.env.NEXT_PUBLIC_HOSTNAME}`}
        />
        <meta content="Streamlit Docs" property="og:title" />
        <meta content="Streamlit Docs" name="twitter:title" />
        {description && (
          <React.Fragment>
            <meta content={description} name="description" />
            <meta content={description} property="og:description" />
            <meta content={description} name="twitter:description" />
          </React.Fragment>
        )}
        <meta property="og:type" content="website" />
        <meta property="og:url" content="https://docs.streamlit.io/" />
        <meta content="summary_large_image" name="twitter:card" />
        <meta
          property="og:image"
          content={`https://${process.env.NEXT_PUBLIC_HOSTNAME}/sharing-image-facebook.jpg`}
        />
        <meta
          name="twitter:image"
          content={`https://${process.env.NEXT_PUBLIC_HOSTNAME}/sharing-image-twitter.jpg`}
        />
      </Head>
      {isTelemetryModalVisible && (
        <CookieSettingsModal
          setIsTelemetryModalVisible={setIsTelemetryModalVisible}
          allowTelemetryAndCloseBanner={allowTelemetryAndCloseBanner}
          declineTelemetryAndCloseBanner={declineTelemetryAndCloseBanner}
        />
      )}
      <GDPRBanner
        isTelemetryModalVisible={isTelemetryModalVisible}
        setIsTelemetryModalVisible={setIsTelemetryModalVisible}
        isTelemetryBannerVisible={isTelemetryBannerVisible}
        setIsTelemetryBannerVisible={setIsTelemetryBannerVisible}
        insertTelemetryCode={insertTelemetryCode}
        setInsertTelemetryCode={setInsertTelemetryCode}
        allowTelemetryAndCloseBanner={allowTelemetryAndCloseBanner}
        declineTelemetryAndCloseBanner={declineTelemetryAndCloseBanner}
      />
      <section className={styles.Container}>
        <SideBar menu={menu} slug={[]} />
        <section className={styles.InnerContainer}>
          <article>
            <H1>Streamlit documentation</H1>
            <p>
              <a href="https://www.streamlit.io">Streamlit</a> is an open-source
              Python framework for data scientists and AI/ML engineers to
              deliver dynamic data apps with only a few lines of code. Build and
              deploy powerful data apps in minutes. Let's get started!
            </p>

            <Spacer size="2rem" />

            <SummaryTiles />

            {/* <H2 className='no-b-m'>What's new</H2>

            <TileContainer>
              <Tile size="half" background="unset" color="unset" dark={{ background: "unset", color: 'white', border_color: 'gray-90' }} border_color="gray-40" img="/logo.svg" title="Feature title" text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Eleifend a facilisis sagittis, vitae nibh massa in facilisis et. Pretium eget non cursus purus tempus porta sodales." link="/tutorials/get-started" />
              <Tile size="half" background="unset" color="unset" dark={{ background: "unset", color: 'white', border_color: 'gray-90' }} border_color="gray-40" icon="visibility" title="Feature title" text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Eleifend a facilisis sagittis, vitae nibh massa in facilisis et. Pretium eget non cursus purus tempus porta sodales." link="/tutorials/get-started" />
              <Tile size="half" background="unset" color="unset" dark={{ background: "unset", color: 'white', border_color: 'gray-90' }} border_color="gray-40" icon="edit" title="Feature title" text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Eleifend a facilisis sagittis, vitae nibh massa in facilisis et. Pretium eget non cursus purus tempus porta sodales." link="/tutorials/get-started" />
              <Tile size="half" background="unset" color="unset" dark={{ background: "unset", color: 'white', border_color: 'gray-90' }} border_color="gray-40" img="/logo.svg" title="Feature title" text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Eleifend a facilisis sagittis, vitae nibh massa in facilisis et. Pretium eget non cursus purus tempus porta sodales." link="/tutorials/get-started" />
            </TileContainer> */}

            <H2>How to use our docs</H2>
            <InlineCalloutContainer>
              <InlineCallout
                color="orange-70"
                icon="rocket_launch"
                bold="Get started"
                href="/get-started"
              >
                with Streamlit! Set up your development environment and learn
                the fundamental concepts, and start coding!
              </InlineCallout>
              <InlineCallout
                color="indigo-70"
                icon="description"
                bold="Develop"
                href="/develop"
              >
                your Streamlit app! Our API reference explains each Streamlit
                function with examples. Dive deep into all of our features with
                conceptual guides. Try out our step-by-step tutorials.
              </InlineCallout>
              <InlineCallout
                color="lightBlue-70"
                icon="cloud"
                bold="Deploy"
                href="/deploy"
              >
                your Streamlit app! Streamlit Community Cloud our free platform
                for deploying and sharing Streamlit apps. Streamlit in Snowflake
                is an enterprise-class solution where you can house your data
                and apps in one, unified, global system. Explore all your
                options!
              </InlineCallout>
              <InlineCallout
                color="darkBlue-70"
                icon="school"
                bold="Knowledge base"
                href="/knowledge-base"
              >
                is a self-serve library of tips, tricks, and articles that
                answer your questions about creating and deploying Streamlit
                apps.
              </InlineCallout>
              {/* <InlineCallout color="green-70" icon="code" bold="Cookbook" href="/cookbook">
                provides short code snippets that you can copy in for specific use cases.
              </InlineCallout>
              <InlineCallout color="red-70" icon="question_answer" bold="Support" href="/support">
                are the bread and butter of how our APIs and configuration files work and will give you short, actionable explanations of specific functions and features.
              </InlineCallout> */}
            </InlineCalloutContainer>

            <H2 className="no-b-m">What's new</H2>

            <TileContainer>
              <RefCard
                size="third"
                href="/develop/api-reference/execution-flow/st.dialog"
              >
                <i className="material-icons-sharp">crop_7_5</i>
                <h4>Modal dialogs</h4>
                <p>
                  Introducing <code>st.experimental_dialog</code> to create
                  modal dialogs that can rerun independently from the rest of
                  your app.
                </p>
              </RefCard>
              <RefCard
                size="third"
                href="https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Outlined"
              >
                <i className="material-icons-sharp">info</i>
                <h4>Google Material Symbols</h4>
                <p>
                  <code>st.toast</code>, <code>st.chat_message</code>, and alert
                  messages now support Material Symbols for their icons.
                </p>
              </RefCard>
              <RefCard
                size="third"
                href="/develop/api-reference/text/st.markdown"
              >
                <i className="material-icons-sharp">highlight</i>
                <h4>Markdown support for text highlighting</h4>
                <p>
                  You can set the background color for you text in markdown.
                </p>
              </RefCard>
              <RefCard
                size="third"
                href="/develop/api-reference/media/st.video"
              >
                <i className="material-icons-sharp">videocam</i>
                <h4>Media autoplay</h4>
                <p>
                  You can enable autoplay for <code>st.audio</code> and
                  <code>st.video</code>. You can also mute videos.
                </p>
              </RefCard>
              <RefCard
                size="third"
                href="/develop/api-reference/caching-and-state/st.cache_data#cachedfuncclear"
              >
                <i className="material-icons-sharp">cached</i>
                <h4>Clear specific cached values</h4>
                <p>
                  When clearing cached values for a function, you can now pass
                  function arguments to clear a specific cached value.
                </p>
              </RefCard>
              <RefCard
                size="third"
                href="/develop/api-reference/caching-and-state/st.query_params#stquery_paramsfrom_dict"
              >
                <i className="material-icons-sharp">question_mark</i>
                <h4>
                  <code>st.query_params.from_dict()</code>
                </h4>
                <p>
                  You can now set all query parameters with a single command.
                </p>
              </RefCard>
              {/* <Tile
                size="half"
                background="unset"
                color="unset"
                dark={{
                  background: "unset",
                  color: "white",
                  border_color: "gray-90",
                }}
                border_color="gray-40"
                img="/logo.svg"
                title="Clear memo + singleton caches procedurally"
                text="Do you need more control over cache invalidation? Any function annotated with @st.cache_data or @st.cache_resource gets its own clear() function automatically."
                link="/develop/concepts/architecture/experimental-cache-primitives#clear-memo-and-singleton-caches-procedurally"
              /> */}
              {/* Preserve above comment for syntax reference */}
            </TileContainer>

            <H2 className="no-b-m">Latest blog posts</H2>

            <NewsContainer>
              <NewsFeed />

              <Button link="https://blog.streamlit.io/" target="_blank">
                View all updates
              </Button>
            </NewsContainer>

            <NoteSplit
              background="gray-20"
              title="Join the community"
              copy="Streamlit is more than just a way to make data apps, it's also a community of creators that share their apps and ideas and help each other make their work better. Please come join us on the community forum. We love to hear your questions, ideas, and help you work through your bugs — stop by today!"
              button={{
                text: "View forum",
                link: "https://discuss.streamlit.io",
                target: "_blank",
              }}
              image="/join.png"
            />
          </article>

          <SocialCallouts />

          <ArrowLinkContainer>
            <ArrowLink link="/get-started" type="next" content="Get started" />
          </ArrowLinkContainer>
        </section>
        <Footer setIsTelemetryModalVisible={setIsTelemetryModalVisible} />
      </section>
    </Layout>
  );
}

export async function getStaticProps(context) {
  const props = {};
  props["menu"] = getMenu();

  return {
    props: props,
  };
}
