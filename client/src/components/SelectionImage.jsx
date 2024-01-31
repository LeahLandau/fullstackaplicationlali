import React, { useEffect, useState } from 'react';
import { createUseStyles } from 'react-jss';
import axios from 'axios';
import 'devextreme/dist/css/dx.light.css';
import TreeView from 'devextreme-react/tree-view';

import { ServerConfig } from '../configs/server';
import Error from './Error';


const useStyles = createUseStyles({
  wrraper: {
    textAlign: 'center',
    width: '350px'
  }
});

const SelectionImage = ({ setImagePath, setIsImages }) => {

  const css = useStyles();

  const [imagesList, setImagesList] = useState([]);
  const [isError, setIsError] = useState(false);
  const [error, setError] = useState('');
  useEffect(() => {

    const changeDataArrayToObject = (arr, num, val = '', parentId = '') => {

      const volume_length = (ServerConfig.VOLUME_NAME).split('/').length;
      const ExtractingNames = arr.map((item) => {
        const splitBySlash = item.split('/').slice(num + volume_length);
        return splitBySlash[0];
      });
      const arrWithoutMulti = ExtractingNames.filter((value, index) => ExtractingNames.indexOf(value) === index);

      return arrWithoutMulti.map((item, index) => {
        const itemId = parentId !== '' ? `${parentId}.${index + 1}` : `${index + 1}`;
        const path = `${val}/${item}`;
        const pathStart = path.startsWith('/') ? path : `/${path}`;
        const arrayFiltered = arr.filter((element) => element.startsWith(`${ServerConfig.VOLUME_NAME}${pathStart}`));
        const isFolder = item.endsWith('.jp2') ? false : true;
        const objectWithId = { name: item, path: path, isFolder: isFolder, id: itemId };
        return isFolder
          ? { ...objectWithId, items: changeDataArrayToObject(arrayFiltered, num + 1, path, itemId) }
          : objectWithId;
      });
    };

    const get_images_names = async () => {
      try {
        const response = await axios.get(`${ServerConfig.PATH}/get_images_names?directory_path=${ServerConfig.VOLUME_NAME}`);
        if (response.data.length !== 0) {
          return changeDataArrayToObject(response.data, 0);
        }
        return [];
      } catch (error) {
        const parser = new DOMParser();
        const doc = parser.parseFromString(error.response.data, 'text/html');
        setError(doc.querySelector('p').textContent);
        setIsError(true);
      }
    };

    const cachedNames = sessionStorage.getItem('images_names');
    setIsImages(false);
    if (cachedNames) {
      const imagesNames = JSON.parse(cachedNames);
      setImagesList(imagesNames);
    } else {
      const updateStorage = async () => {
        const imagesNames = await get_images_names();
        if (imagesNames) {
          sessionStorage.setItem('images_names', JSON.stringify(imagesNames));
          setImagesList(imagesNames);
        }
      };
      updateStorage();
    }
  }, [setIsImages]);

  const selectItem = (e) => {
    const clickedNode = e.itemData;
    console.log(clickedNode);
    const updateNode = (node, nodeID) => {
      console.log(node ,nodeID);
      if (node.id === nodeID) {
        return { ...node, expanded: !node.expanded };
      }
      if (node.items && node.items.length > 0) {
        const updatedItems = node.items.map((item) => {
          return updateNode(item, nodeID);
        });
        return { ...node, items: updatedItems };
      }
      return node;
    };
    const updatedData = imagesList.map((node) => updateNode(node, clickedNode.id));
    setImagesList(updatedData);
    if (!clickedNode.isFolder) {
      const path = clickedNode.path;
      setImagePath(`${ServerConfig.VOLUME_NAME}${path}`);
      setIsImages(true);
    }
  };
  return <>
    {!isError ? <div className={css.wrraper}>
      <TreeView
        keyExpr='id'
        displayExpr='name'
        dataSource={imagesList}
        searchEnabled={true}
        selectionMode='single'
        selectByClick={true}
        onItemSelectionChanged={selectItem}
      />
    </div> : <Error response={`${error}`}></Error>
    }
  </>;
};

export default SelectionImage;
