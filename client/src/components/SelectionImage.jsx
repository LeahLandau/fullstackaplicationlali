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
})

const SelectionImage = ({ setImagePath, setIsImages }) => {

    const css = useStyles();

    const [imagesList, setImagesList] = useState([])
    const [isError, setIsError] = useState(false)
    const [error, setError] = useState('')
    useEffect(() => {

        const changeDataArrayToObject = (arr, num, val = '') => {

            const ExtractingNames = arr.map((item) => {
                const splitBySlash = item.split("/").slice(num + 3)
                return splitBySlash[0]
            })
            const arrWithoutMulti = ExtractingNames.filter((value, index) => ExtractingNames.indexOf(value) === index)

            return arrWithoutMulti.map((item) => {
                const path = `${val}/${item}`;
                const pathStart = path.startsWith('/') ? path : `/${path}`;
                const arrayFiltered = arr.filter((element) => element.startsWith(`/static/images${pathStart}`));
                return (item.endsWith(".jp2")) ? { name: item, path: path, isFolder: false } :
                    { name: item, path: path, isFolder: true, items: changeDataArrayToObject(arrayFiltered, num + 1, path) };
            });
        }

        const get_images_names = async () => {
            try {
                const response = await axios.get(`${ServerConfig.PATH}/get_images_names?directory_path=/images`)
                if (response.data.length !== 0) {
                    setIsImages(true);
                    return changeDataArrayToObject(response.data, 0);
                }
                setIsImages(false);
                return []
            } catch (error) {
                const parser = new DOMParser();
                const doc = parser.parseFromString(error.response.data, "text/html");
                setError(doc.querySelector("p").textContent);
                setIsError(true)
            }
        }

        const cachedNames = sessionStorage.getItem('images_names');
        if (cachedNames) {
            const imagesNames = JSON.parse(cachedNames);
            setImagesList(imagesNames);
            if(imagesNames.length !== 0)
                setIsImages(true)
        } else {
            const updateStorage = async () => {
                const imagesNames = await get_images_names();
                if (imagesNames) {
                    sessionStorage.setItem('images_names', JSON.stringify(imagesNames));
                    setImagesList(imagesNames);
                }
            }
            updateStorage();
        }
    }, [setIsImages])

    const selectItem = (e) => {
        const clickedNode = e.itemData;
        const updateNode = (node, nodeName) => {
            if (node.name === nodeName) {
                return { ...node, expanded: !node.expanded };
            }
            if (node.items && node.items.length > 0) {
                const updatedItems = node.items.map((item) => {
                    return updateNode(item, nodeName);
                });
                return { ...node, items: updatedItems };
            }
            return node;
        };
        const updatedData = imagesList.map((node) => updateNode(node, clickedNode.name));
        setImagesList(updatedData);
        if (!clickedNode.isFolder) {
            const path = clickedNode.path
            setImagePath(`/images${path}`)
        }
    };
    return <>
        {!isError ? <div className={css.wrraper}>
            <TreeView
                keyExpr="name"
                displayExpr="name"
                dataSource={imagesList}
                searchEnabled={true}
                selectionMode="single"
                selectByClick={true}
                onItemSelectionChanged={selectItem}
            />
        </div> : <Error response={`${error}`}></Error>
        }
    </>
}

export default SelectionImage;