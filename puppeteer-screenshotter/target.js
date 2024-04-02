import * as puppeteer from 'puppeteer';

function sleep(time) {
  return new Promise(function (resolve) {
    setTimeout(resolve, time);
  });
}

export async function FetchScreenie() {
  let browser;
  try {
    browser = await puppeteer.launch({
      headless: 'new',
      args: ['--no-sandbox', '--disable-gpu', '--disable-setuid-sandbox'],
    });
    const page = await browser.newPage();

    // set screen size (HD Portrait)
    await page.setViewport({ width: 1080, height: 1920 });

    await page.goto('https://www.theguardian.com/international', {
      timeout: 10000, // give it 10 seconds to load
      waitUntil: 'networkidle2',
    });

    // example actions for page preparation (e.g. loading modal etc)
    await sleep(500); // force blocking wait
    // get rid of cookie notice if present
    const CookieMessageSelectorExists = await page.$(
      'button.message-component:nth-child(1)'
    );
    if (CookieMessageSelectorExists) {
      await page.click('button.message-component:nth-child(1)');
    }

    // wait for relevant section to load
    await page.$('gu-island', {
      timeout: 10000, // give it 10 seconds to load
      waitUntil: 'networkidle2',
    });

    // save screenshot directly to filepath
    // await page.screenshot({ path: 'screenshot.png' });

    // get screenshot of designated region as buffer
    const image = await page.screenshot({
      type: 'jpeg',
      quality: 100,
      clip: {
        x: 0,
        y: 167,
        width: 1080,
        height: 150,
      },
      omitBackground: true,
    });

    const base64Image = await image.toString('base64');

    return base64Image;
  } catch (error) {
    console.error('Failed to load page: ', error);
    return error;
  } finally {
    if (browser) await browser.close();
  }
}
