import { FetchScreenie } from './target.js';
import fs from 'fs';

(async () => {
  console.log('Generating screenshot...');
  const image = await FetchScreenie();
  if (typeof image === 'string') {
    console.log(
      `${image.substring(0, 12)}...${image.substring(image.length - 8)}`
    );
    const decodedImage = Buffer.from(image, 'base64');
    fs.writeFileSync('screenshot.jpg', decodedImage, { flag: 'w' });
    console.log('saved screenshot.jpg');
  } else {
    console.error(`Error capturing screenshot: ${image?.message}`);
  }
})();
