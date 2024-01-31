
export const ServerConfig = {
  PATH:  process.env.REACT_APP_SERVER_PATH ||`${window.location.href}api`,
  VOLUME_NAME:process.env.REACT_APP_IMAGES_VOLUME_NAME ||'/images'
};
