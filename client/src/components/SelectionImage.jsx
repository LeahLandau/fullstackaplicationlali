import React, { useContext, useEffect, useState } from 'react';

import 'devextreme/dist/css/dx.light.css';
import TreeView from 'devextreme-react/tree-view';

import ImgContext from '../context/ImageReduction';
import axios from 'axios';
import { ServerConfig } from '../configs/server';

const SelectionImage = () => {

    const { setImagePath } = useContext(ImgContext)
    const [data, setData] = useState([])

    const createObject = (arr, num, val = '') => {

        const arrSplit = arr.map((item) => {
            const element = item.split("/").slice(num + 2)
            return element[0]
        })
        const arrWithoutMulti = arrSplit.filter((value, index) => arrSplit.indexOf(value) === index)

        return arrWithoutMulti.map((item) => {
            const path = `${val}/${item}`;
            const pathStart = path.startsWith('/') ? path : '/' + path;
            const arrFiltered = arr.filter((element) => element.startsWith(`/images${pathStart}`));
            return (item.endsWith(".jpg")) || (item.endsWith(".jp2")) ? { name: item, path: path, isFolder: false } :
                { name: item, path: path, isFolder: true, items: createObject(arrFiltered, num + 1, path) };
        });
    }

    useEffect(() => {
        const get_images_names = async () => {
            const response = await axios.get(`${ServerConfig.PATH}/get_images_names?directory_path=/images`)
            if (Array.isArray(response.data)) {
                const hierarchical = response.data;
                if (response.data !== []) {
                    const correctObject = createObject(hierarchical, 0);
                    setData(correctObject);
                }
            } else {
                console.log(response.data);
            }
        }
        get_images_names()
    }, [])

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
                return { ...node, items: updatedItems, };
            }
            return node;
        };
        const updatedData = data.map((node) => updateNode(node, clickedNode.name));
        setData(updatedData);

        if (!clickedNode.isFolder) {
            const path = clickedNode.path
            setImagePath(`http://localhost:8080/images${path}`)
        }
    };

    return <>
        <TreeView
            keyExpr="name"
            displayExpr="name"
            dataSource={data}
            searchEnabled={true}
            selectionMode="single"
            selectByClick={true}
            onItemSelectionChanged={selectItem}
        />
    </>

}

export default SelectionImage;