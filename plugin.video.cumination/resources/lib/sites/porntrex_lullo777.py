import re
from six.moves import urllib_parse, urllib_error

import xbmc
from resources.lib import utils
from resources.lib.adultsite import AdultSite
from resources.lib import basics

site = AdultSite(name='porntrex_lullo777', title='[COLOR hotpink]Porntrex_lullo777[/COLOR]', url='https://www.porntrex.com/', image='pt.png', about='porntrex')

getinput = utils._get_keyboard
ptlogged = 'true' in utils.addon.getSetting(id='ptlogged')
lengthChoices = {'All': '', '0-10 min': 'ten-min/', '10-30 min': 'ten-thirty-min/', '30+': 'thirty-all-min/'}
qualityChoices = {'All': '', '4k': '4k', '1080p+': '4k, 1440p, 1080p', '720p+': '4k, 1440p, 1080p, 720p, HD', '1080p': '1080p', '720p': '720p'}
sortChoices = {'Time': 'No', 'Name': 'sorted_name', 'Duration': 'sorted_duration', 'Duration Reverse': 'sorted_duration_reverse', 'Views': 'sorted_views', 'Rating': 'sorted_rating', 'Time Reverse': 'sorted_time_reverse'}
private_videoChoices = {'Latest': 'post_date', 'Most Viewed': 'video_viewed', 'Top Rated': 'rating', 'Longest': 'duration', 'Most Commented': 'most_commented', 'Most Favourited': 'most_favourited'}

ptlength = utils.addon.getSetting(id='ptlength') or 'All'
ptquality = utils.addon.getSetting(id='ptquality') or 'All'
ptsubscription = utils.addon.getSetting(id='ptsubscription') or 'No'
ptinfovideos = utils.addon.getSetting(id='ptinfovideos') or 'No'
ptrange = utils.addon.getSetting(id='ptrange') or 'No'
ptrangesort = utils.addon.getSetting(id='ptrangesort') or 'No'

debugurl = True

@site.register(default_mode=True)
def PTMain():
    site.add_dir(name='[COLOR hotpink]Length: [/COLOR] [COLOR orange]{0}[/COLOR]'.format(ptlength), url='', mode='PTLength', iconimage='', Folder=False)
    site.add_dir(name='[COLOR hotpink]Filter By Quality: [/COLOR] [COLOR gold]{0}[/COLOR]'.format(ptquality), url='', mode='PTFilterByQuality', iconimage='', Folder=False)
    if ptlogged:
        site.add_dir(name='[COLOR hotpink]Select Range: [/COLOR] [COLOR orange]{0}[/COLOR]'.format(ptrange), url='', mode='PTSetRange', iconimage='', Folder=False)
    site.add_dir(name='[COLOR hotpink]Categories[/COLOR]', url='{0}categories/?mode=async&function=get_block&block_id=list_categories_categories_list&sort_by=title&from=1'.format(site.url), mode='PTCat', iconimage=site.img_cat)
    site.add_dir(name='[COLOR hotpink]Most Viewed This Week[/COLOR]', url='{0}most-popular/weekly/{1}'.format(site.url, lengthChoices[ptlength]), page=1, mode='PTList')
    if ptlogged:
        url_models = '{0}models/1/?mode=async&function=get_block&block_id=list_models_models_list&sort_by=total_videos&from=1'.format(site.url)
        url_members = '{0}members/?mode=async&function=get_block&block_id=list_members_members&sort_by=video_viewed&from_members=1'.format(site.url)
        url_playlists = '{0}playlists/?mode=async&function=get_block&block_id=list_playlists_common_playlists_list&sort_by=playlist_viewed&from=1'.format(site.url)
        site.add_dir(name='[COLOR hotpink]Models[/COLOR]', url=url_models, page=1, mode='PTModels')
        site.add_dir(name='[COLOR hotpink]Members[/COLOR]', url=url_members, page=1, mode='PTMembers')
        site.add_dir(name='[COLOR hotpink]Playlists[/COLOR]', url=url_playlists, page=1, mode='PTPlaylists')
    site.add_dir(name='[COLOR hotpink]Search[/COLOR]', url='{0}search/'.format(site.url), mode='PTSearch', iconimage=site.img_search)
    if not ptlogged:
        site.add_dir(name='[COLOR hotpink]Login[/COLOR]', url='', mode='PTLogin', iconimage='', Folder=False)
    elif ptlogged:
        site.add_dir(name='[COLOR hotpink]Porntrex account (favorites, subscriptions)[/COLOR]', url='', mode='PTAccount', iconimage='')
    ptlist = PTList(url='{0}latest-updates/{1}'.format(site.url, lengthChoices[ptlength]), page=1)
    if not ptlist:
        utils.eod()


@site.register()
def PTAccount():
    ptuser = utils.addon.getSetting(id='ptuser')
    url_sub_v = '{0}my/subscriptions/?mode=async&function=get_block&block_id=list_videos_videos_from_my_subscriptions&sort_by=&from_my_subscriptions_videos=1'.format(site.url)
    url_sub = '{0}my/subscriptions/?mode=async&function=get_block&block_id=list_members_subscriptions_my_subscriptions&sort_by=added_date&from_my_subscriptions=1'.format(site.url)
    url_prv = '{0}private/1/?mode=async&function=get_block&block_id=list_videos_common_videos_list_norm&sort_by=post_date&from4=1'.format(site.url)
    url_his = '{0}my/history/?mode=async&function=get_block&block_id=list_videos_my_history_videos&fav_type=&playlist_id=0&sort_by=&from17=1'.format(site.url)
    url_fav = '{0}my/favourites/videos/?mode=async&function=get_block&block_id=list_videos_my_favourite_videos&fav_type=0&playlist_id=0&sort_by=&from_my_fav_videos=1'.format(site.url)
    if ptrange == 'No':
        site.add_dir2(name='[COLOR hotpink]Subscription videos[/COLOR]', url=url_sub_v, page=1, mode='PTList', desc=set_trim_url(url=url_sub_v))
        site.add_dir2(name='[COLOR hotpink]PTSubscriptions[/COLOR]', url=url_sub, page=1, mode='PTSubscriptions', desc=set_trim_url(url=url_sub))
        site.add_dir2(name='[COLOR hotpink]Video History[/COLOR]', url=url_his, page=1, mode='PTList', desc=set_trim_url(url=url_his))
        site.add_dir2(name='[COLOR violet]PT Favorites[/COLOR]', url=url_fav, page=1, mode='PTList', desc=set_trim_url(url=url_fav))
    else:
        site.add_dir2(name='[COLOR hotpink]Subscription videos[/COLOR]', url=url_sub_v, page=1, mode='PTListSort', onelist=12, desc=set_trim_url(url=url_sub_v))
        site.add_dir2(name='[COLOR hotpink]PTSubscriptions[/COLOR]', url=url_sub, page=1, mode='PTRangeList', onelist=10, section='PTSubscriptions', desc=set_trim_url(url=url_sub))
        site.add_dir2(name='[COLOR hotpink]Video History[/COLOR]', url=url_his, page=1, mode='PTListSort', onelist=4, desc=set_trim_url(url=url_his))
        site.add_dir2(name='[COLOR violet]PT Favorites[/COLOR]', url=url_fav, page=1,  mode='PTListSort', onelist=4, desc=set_trim_url(url=url_fav))
    site.add_dir2(name='[COLOR hotpink]Private Videos[/COLOR]', url=url_prv, page=1, mode='PTList', desc=set_trim_url(url=url_prv))
    site.add_dir2(name='[COLOR hotpink]PTAscii Files[/COLOR]', url='', mode='PTAsciiFiles')
    site.add_dir(name='[COLOR hotpink]Logout {0}[/COLOR]'.format(ptuser), url='', mode='PTLogin', iconimage='', Folder=False)
    utils.eod(cache=False)


@site.register()
#load ascii files from profile directory
def PTAsciiFiles():
    site.add_dir2(name='[COLOR hotpink]Ascii Tags[/COLOR]', url='tags_list.txt', mode='OpenAsciiFile', section='tags', sort='sorted_name', desc='tags_list.txt')
    site.add_dir2(name='[COLOR hotpink]Ascii Studios Tags[/COLOR]', url='tags_studios.txt', mode='OpenAsciiFile', section='tags', sort='sorted_name', desc='tags_studios.txt')
    site.add_dir2(name='[COLOR hotpink]Ascii Tags Models[/COLOR]', url='tag_model_list.txt', mode='OpenAsciiFile', section='tags', sort='sorted_name', desc='tag_model_list.txt')
    site.add_dir2(name='[COLOR hotpink]Ascii Models[/COLOR]', url='model_list.txt', mode='OpenAsciiFile', section='models', sort='sorted_name', desc='model_list.txt')
    utils.eod(cache=False)


@site.register()
def PTLength():
    input = utils.selector(dialog_name='Select Length', select_from=lengthChoices.keys())
    if input:
        utils.addon.setSetting(id='ptlength', value=input)
        xbmc.executebuiltin(function='Container.Refresh')


@site.register()
def PTFilterByQuality():
    input = utils.selector(dialog_name='Pick a quality to filter videos', select_from=qualityChoices.keys(), show_on_one=True)
    if input:
        utils.addon.setSetting(id='ptquality', value=input)
        xbmc.executebuiltin(function='Container.Refresh')


@site.register()
#make use of PTRangeList and PTListSort
def PTSetRange():
    input = utils.selector(dialog_name='Select Range', select_from=['Yes', 'No'], show_on_one=True)
    if input:
        utils.addon.setSetting(id='ptrange', value=input)
        xbmc.executebuiltin(function='Container.Refresh')


@site.register()
def PTGetInfoVideos(url, page):
    utils.addon.setSetting(id='ptinfovideos', value='Yes')
    ptlist = PTList(url=url, page=page)
    if not ptlist:
        utils.eod()


@site.register()
def PTList(url, page=1, onelist=None):
    global list_html
    if onelist:
        url = url.replace('/1/', '/' + str(page) + '/')
        url = strip_end(text=url, suffix='=' + str(1)) + '=' + str(page)
    hdr = dict(utils.base_hdrs)
    hdr['Cookie'] = get_cookies()
    try:
        list_html = utils._getHtml(url=url, referer=site.url, headers=hdr, error='raise')
    except urllib_error.HTTPError as e:
        if e.code == 403:
            if PTLogin(logged=False):
                hdr['Cookie'] = get_cookies()
                list_html = utils._getHtml(url=url, referer=site.url, headers=hdr)
    if ptlogged and ('>Log in<' in list_html):
        if PTLogin(logged=False):
            hdr['Cookie'] = get_cookies()
            list_html = utils._getHtml(url=url, referer=site.url, headers=hdr)
        else:
            return None

    if not any(s in url for s in ['/members/', '/subscriptions/', '/my/', '/video/']) and page == 1:
        if '/search/' in url:
            strip_url = set_strip_sort_url(url=url, int_split=4)
            site.add_dir2(name='[COLOR hotpink]Sort Videos: [/COLOR][COLOR orange]{0}[/COLOR]'.format(strip_url), url=url, mode='PTSet_sort_by_videos_search', desc=set_trim_url(url=url))
        elif '/private/' in url:
            strip_url = set_strip_sort_url(url=url, int_split=3)
            site.add_dir2(name='[COLOR hotpink]Sort Videos: [/COLOR][COLOR orange]{0}[/COLOR]'.format(strip_url), url=url, mode='PTSet_sort_by_private_videos', desc=set_trim_url(url=url))
        else:
            #reset pt_category
            utils.addon.setSetting(id='pt_category', value=None)
            if any(s in url for s in ['/models/', '/categories/', '/tags/']):
                int_split = 4
            else:
                int_split = 3
            strip_url = set_strip_sort_url(url=url, int_split=int_split)
            site.add_dir2(name='[COLOR hotpink]Sort Videos: [/COLOR][COLOR orange]{0}[/COLOR]'.format(strip_url), url=url, mode='PTSet_sort_by_videos', desc=set_trim_url(url=url))
    if ptlogged:
        if not onelist:
            site.add_dir(name='[COLOR hotpink]Get Extra Info Videos: [/COLOR]', url=url, mode='PTGetInfoVideos', iconimage='', page=page)
    match = re.compile(pattern='data-item-id=.*?href="([^"]+)".*?data-src="([^"]+)"(.*?)<div class="hd-text-icon(.*?)<div class="viewsthumb">([\d ]+) views</div>.*?clock-o"></i> ([^<]+)<.*?title="([^"]+)".*?<ul class="list-unstyled"><li>([^"]+)</li><li class="pull-right"><i class="fa fa-thumbs-o-up"></i> ([\d%]+)</li>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
    if page == 1:
        if '{0}my/'.format(site.url) in url or '{0}members/'.format(site.url) in url:
            set_fav_selector(url=url)
    for video_page, img, private, hd, views, duration, name, time, rating in match:
        name = utils.cleantext(name)
        hd = resolve_hd(hd=hd)
        if 'private' in private.lower():
            if not ptlogged:
                continue
            private = "[COLOR blue][PV][/COLOR] "
        else:
            private = ""

        if ptquality != 'All':
            if hd not in qualityChoices[ptquality]:
                continue

        desc = '[COLOR deeppink]Views:[/COLOR] ' + views
        desc += '\n[COLOR deeppink]Time:[/COLOR] ' + time
        desc += '\n[COLOR deeppink]Rating:[/COLOR] ' + rating

        img = resolve_img(img=img)
        str_name = "[COLOR deeppink]{0}[/COLOR] {1} {2} [COLOR orange]{3}[/COLOR]".format(duration, private, name, hd)
        contextmenu = []
        if ptlogged:
            if '{0}my/favourites/videos/'.format(site.url) in url and 'fav_type=0' in url and 'playlist_id=0' in url:
                contextmenu.append(('[COLOR violet]Delete from PT favorites[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTContextMenu&url={2}&fav=del_fav'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(video_page))+')'))
            else:
                contextmenu.append(('[COLOR violet]Add to PT favorites[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTContextMenu&url={2}&fav=add_fav'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(video_page))+')'))
            if '{0}my/favourites/videos/'.format(site.url) in url and 'fav_type=1' in url and 'playlist_id=0' in url:
                contextmenu.append(('[COLOR hotpink]Delete from PT watch later[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTContextMenu&url={2}&fav=del_w_later'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(video_page))+')'))
            else:
                contextmenu.append(('[COLOR hotpink]Add to PT watch later[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTContextMenu&url={2}&fav=add_w_later'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(video_page))+')'))
            contextmenu.append(('[COLOR hotpink]Add to PT playlist[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTCheck_playlists&url={2}&fav=add_to_playlist'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(video_page))+')'))
            if '{0}my/favourites/videos/'.format(site.url) in url and 'fav_type=10' in url:
                filtered = re.findall(pattern='playlist_id=(\d+)', string=url)[0]
                contextmenu.append(('[COLOR hotpink]Move to PT playlist[/COLOR]', 'RunPlugin('+'{0}?mode={1}PTCheck_playlists&url={2}&fav=move_to_playlist&filtered={3}'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(video_page), str(filtered))+')'))
                contextmenu.append(('[COLOR hotpink]Delete from PT playlist[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTContextMenu&url={2}&fav=del_from_playlist&filtered={3}'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(video_page), str(filtered))+')'))
            contextmenu.append(('[COLOR hotpink]GetInfo Video[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTGetInfoVideoTextBox&url={2}&desc={3}'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(video_page), str(desc))+')'))
            contextmenu.append(('[COLOR hotpink]Lookup tags[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTCheck_tags&url={2}'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(video_page))+')'))
            contextmenu.append(('[COLOR hotpink]Lookup models[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTCheck_models&url={2}'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(video_page))+')'))
            contextmenu.append(('[COLOR hotpink]Check member[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTCheck_member&url={2}'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(video_page))+')'))
            contextmenu.append(('[COLOR hotpink]Related Videos[/COLOR]', 'Container.Update('+'{0}?mode={1}.PTList&url={2}&page=1'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(video_page))+')'))
            if utils.addon.getSetting(id='ptinfovideos') == 'Yes':
                info_video = PTGetInfoVideo(url=video_page)
                if info_video:
                    desc = info_video + '\n' + desc
        site.add_download_link(name=str_name, url=video_page, mode='PTPlayvid', iconimage=img, desc=desc, contextm=contextmenu)
    utils.addon.setSetting(id='ptinfovideos', value='No')

    if not onelist:
        if ptlogged:
            if any(s in url for s in ['/models/', '/categories/', '/tags/', '/search/']):
                section = get_section_from_url(url=url)
                tag_section = get_next_folder_from_url(url=url, folder=section, int=1)
                if '/models/' in url or '-' not in tag_section:
                    if any(s in url for s in ['/models/', '/categories/']):
                        url_tag = '{0}tags/{1}/{2}?mode=async&function=get_block&block_id=list_videos_common_videos_list_norm&sort_by=post_date&from4=1'.format(site.url, tag_section, lengthChoices[ptlength])
                        site.add_dir2(name='[COLOR hotpink]Tag[/COLOR]', url=url_tag, page=1, mode='PTList', desc=set_trim_url(url=url_tag))
                        if '/models/' in url and '-' in tag_section:
                            tag_section_clean = tag_section.replace('-', '')
                            url_tag_clean = '{0}tags/{1}/{2}?mode=async&function=get_block&block_id=list_videos_common_videos_list_norm&sort_by=post_date&from4=1'.format(site.url, tag_section_clean, lengthChoices[ptlength])
                            site.add_dir2(name='[COLOR hotpink]Tag clean[/COLOR]', url=url_tag_clean, page=1, mode='PTList', desc=set_trim_url(url=url_tag_clean))
                    if '/search/' not in url:
                        url_search = get_ajax_search_page1_url(url='{0}search/{1}/latest-updates/{2}'.format(site.url, tag_section, lengthChoices[ptlength]))
                        site.add_dir2(name='[COLOR hotpink]Search[/COLOR]', url=url_search, page=1, mode='PTList', desc=set_trim_url(url=url_search))
                    url_search_cat = '{0}search'.format(site.url)
                    site.add_dir2(name='[COLOR hotpink]SearchFilterCategory[/COLOR]', url=url_search_cat, mode='PTSearchFilterCategory', keyword=tag_section, desc=set_trim_url(url=url_search_cat))
        if '/search/' in url:
            page_list_search(url=url, page=page, content=list_html)
        else:
            page_list(url=url, page=page, mode='PTList', content=list_html)
        utils.eod()
        return True


@site.register()
#url = startpage url
#page = startpage number
#onelist = number of pages to 1 page
#section = PTList, PTSubscriptions, PTPlaylists, PTMembers, Friends, PTModels
def PTRangeList(url, page=1, onelist=None, section=None):
    global list_html
    if not page:
        return None
    hdr = dict(utils.base_hdrs)
    hdr['Cookie'] = get_cookies()
    try:
        list_html = utils._getHtml(url=url, referer=site.url, headers=hdr, error='raise')
    except urllib_error.HTTPError as e:
        if e.code == 403:
            if PTLogin(logged=False):
                hdr['Cookie'] = get_cookies()
                list_html = utils._getHtml(url=url, referer=site.url, headers=hdr)
    if re.search(pattern='<li class="last"><a href="', string=list_html, flags=re.DOTALL | re.IGNORECASE):
        last_p = re.compile(pattern='<li class="last"><a href=".*?data-parameters.*?sort_by:[^"]+:(\d+)">', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)[0]
        last_p = int(last_p)
    else:
        last_p = 1
    if not onelist:
        range_page = last_p
    elif int(onelist)+page > last_p:
        range_page = last_p-page+1
    else:
        range_page = int(onelist)
    for page in range(page, range_page+page):
        if section == 'PTList':
            PTList(url=url, page=page, onelist=True)
        elif section == 'PTSubscriptions':
            PTSubscriptions(url=url, page=page, onelist=True)
        elif section == 'PTPlaylists':
            PTPlaylists(url=url, page=page, onelist=True)
        elif section == 'PTMembers':
            PTMembers(url=url, page=page, onelist=True)
        elif section == 'Friends':
            PTMembers(url=url, page=page, onelist=True)
        elif section == 'PTModels':
            PTModels(url=url, page=page, onelist=True)

    n_page = page + 1
    if onelist and n_page <= last_p:
        site.add_dir2(name='[COLOR hotpink]Next Page ('+str(n_page)+'/' + str(last_p) +')[/COLOR]', url=url, mode='PTRangeList', iconimage=site.img_next, page=n_page, onelist=range_page, section=section, desc=set_trim_url(url=url))
    utils.eod()



@site.register()
#url = startpage url
#page = startpage number
#onelist = number of pages to 1 page
def PTListSort(url, page, onelist):
    ptrangesort = utils.addon.getSetting(id='ptrangesort')
    global list_html
    last_p = 1
    hdr = dict(utils.base_hdrs)
    hdr['Cookie'] = get_cookies()
    try:
        list_html = utils._getHtml(url=url, referer=site.url, headers=hdr, error='raise')
    except urllib_error.HTTPError as e:
        if e.code == 403:
            if PTLogin(logged=False):
                hdr['Cookie'] = get_cookies()
                list_html = utils._getHtml(url=url, referer=site.url, headers=hdr)

    site.add_dir2(name='[COLOR hotpink]Sort Videos: [/COLOR][COLOR orange]{0}[/COLOR]'.format(ptrangesort), url=url, page=1, onelist=onelist, mode='PTSet_Listsort_by_videos', desc=set_trim_url(url=url))
    if re.search(pattern='<li class="last"><a href="', string=list_html, flags=re.DOTALL | re.IGNORECASE):
        last_p = re.compile(pattern='<li class="last"><a href=".*?data-parameters.*?sort_by:[^"]+:(\d+)">', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)[0]
        last_p = int(last_p)
    match, n_page = set_pages_to_match_onelist(url=url, page=page, onelist=onelist, list_html=list_html, section='PTList')
    if not match:
        match = re.compile(pattern='data-item-id=.*?href="([^"]+)".*?data-src="([^"]+)"(.*?)<div class="hd-text-icon(.*?)<div class="viewsthumb">([\d ]+) views</div>.*?clock-o"></i> ([^<]+)<.*?title="([^"]+)".*?<ul class="list-unstyled"><li>([^"]+)</li><li class="pull-right"><i class="fa fa-thumbs-o-up"></i> ([\d%]+)</li>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
    if ptrangesort == 'No':
        sort_url = match
    elif ptrangesort == 'sorted_name':
        sort_url = sorted(match, key=lambda x: x[6].lower())
    elif ptrangesort == 'sorted_duration':
        sort_url = sorted(match, key=lambda x: float(x[5].replace(':', '')))
    elif ptrangesort == 'sorted_duration_reverse':
        sort_url = sorted(match, key=lambda x: float(x[5].replace(':', '')), reverse=True)
    elif ptrangesort == 'sorted_views':
        sort_url = sorted(match, key=lambda x: float(x[4].replace(' ', '')), reverse=True)
    elif ptrangesort == 'sorted_rating':
        sort_url = sorted(match, key=lambda x: float(x[8].replace('%', '')), reverse=True)
    elif ptrangesort == 'sorted_time_reverse':
        match.reverse()
        sort_url = match
    else:
        sort_url = match
    if page == 1:
        if '{0}my/'.format(site.url) in url or '{0}members/'.format(site.url) in url:
            set_fav_selector(url=url)
    for video_page, img, private, hd, views, duration, name, time, rating in sort_url:
        name = utils.cleantext(name)
        hd = resolve_hd(hd=hd)
        if 'private' in private.lower():
            if not ptlogged:
                continue
            private = "[COLOR blue][PV][/COLOR] "
        else:
            private = ""

        if ptquality != 'All':
            if hd not in qualityChoices[ptquality]:
                continue

        desc = '[COLOR deeppink]Views:[/COLOR] ' + views
        desc += '\n[COLOR deeppink]Time:[/COLOR] ' + time
        desc += '\n[COLOR deeppink]Rating:[/COLOR] ' + rating

        img = resolve_img(img=img)
        str_name = "[COLOR deeppink]{0}[/COLOR] {1} {2} [COLOR orange]{3}[/COLOR]".format(duration, private, name, hd)
        contextmenu = []
        if ptlogged:
            if '{0}my/favourites/videos/'.format(site.url) in url and 'fav_type=0' in url and 'playlist_id=0' in url:
                contextmenu.append(('[COLOR violet]Delete from PT favorites[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTContextMenu&url={2}&fav=del_fav'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(video_page))+')'))
            else:
                contextmenu.append(('[COLOR violet]Add to PT favorites[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTContextMenu&url={2}&fav=add_fav'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(video_page))+')'))
            if '{0}my/favourites/videos/'.format(site.url) in url and 'fav_type=1' in url and 'playlist_id=0' in url:
                contextmenu.append(('[COLOR hotpink]Delete from PT watch later[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTContextMenu&url={2}&fav=del_w_later'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(video_page))+')'))
            else:
                contextmenu.append(('[COLOR hotpink]Add to PT watch later[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTContextMenu&url={2}&fav=add_w_later'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(video_page))+')'))
            contextmenu.append(('[COLOR hotpink]Add to PT playlist[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTCheck_playlists&url={2}&fav=add_to_playlist'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(video_page))+')'))
            if '{0}my/favourites/videos/'.format(site.url) in url and 'fav_type=10' in url:
                filtered = re.findall(pattern='playlist_id=(\d+)', string=url)[0]
                contextmenu.append(('[COLOR hotpink]Move to PT playlist[/COLOR]', 'RunPlugin('+'{0}?mode={1}PTCheck_playlists&url={2}&fav=move_to_playlist&filtered={3}'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(video_page), str(filtered))+')'))
                contextmenu.append(('[COLOR hotpink]Delete from PT playlist[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTContextMenu&url={2}&fav=del_from_playlist&filtered={3}'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(video_page), str(filtered))+')'))
        contextmenu.append(('[COLOR hotpink]GetInfo Video[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTGetInfoVideoTextBox&url={2}&desc={3}'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(video_page), str(desc))+')'))
        contextmenu.append(('[COLOR hotpink]Lookup tags[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTCheck_tags&url={2}'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(video_page))+')'))
        contextmenu.append(('[COLOR hotpink]Lookup models[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTCheck_models&url={2}'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(video_page))+')'))
        contextmenu.append(('[COLOR hotpink]Check member[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTCheck_member&url={2}'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(video_page))+')'))
        contextmenu.append(('[COLOR hotpink]Related Videos[/COLOR]', 'Container.Update('+'{0}?mode={1}.PTList&url={2}&page=1'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(video_page))+')'))
        site.add_download_link(name=str_name, url=video_page, mode='PTPlayvid', iconimage=img, desc=desc, contextm=contextmenu)
    if onelist and n_page <= last_p:
        url = strip_end(text=url, suffix='=' + str(page)) + '=' + str(n_page)
        site.add_dir2(name='[COLOR hotpink]Next Page ('+str(n_page)+'/' + str(last_p) + ')[/COLOR]', url=url, mode='PTListSort', iconimage=site.img_next, page=n_page, onelist=onelist, desc=set_trim_url(url=url))
    utils.eod()
    return True


@site.register()
def PTPlayvid(url, name, download=None):
    vp = utils.VideoPlayer(name=name, download=download)
    vp.progress.update(25, "[CR]Loading video page[CR]")

    hdr = dict(utils.base_hdrs)
    hdr['Cookie'] = get_cookies()
    video_page = utils._getHtml(url=url, referer=site.url, headers=hdr)

    if 'video_url_text' not in video_page:
        videourl = re.compile(pattern="video_url: '([^']+)'", flags=re.DOTALL | re.IGNORECASE).search(string=video_page).group(1)
    else:
        sources = {}
        srcs = re.compile(pattern="video(?:_alt_|_)url(?:[0-9]|): '([^']+)'.*?video(?:_alt_|_)url(?:[0-9]|)_text: '([^']+)'", flags=re.DOTALL | re.IGNORECASE).findall(string=video_page)
        for src, quality in srcs:
            sources[quality] = src
        videourl = utils.prefquality(video_list=sources, sort_by=lambda x: int(''.join([y for y in x if y.isdigit()])), reverse=True)
    if not videourl:
        vp.progress.close()
        return
    vp.progress.update(75, "[CR]Video found[CR]")
    vp.play_from_direct_link(direct_link=videourl)


@site.register()
def PTCat(url):
    global list_html
    hdr = dict(utils.base_hdrs)
    hdr['Cookie'] = get_cookies()
    try:
        list_html = utils._getHtml(url=url, referer=site.url, headers=hdr, error='raise')
    except urllib_error.HTTPError as e:
        if e.code == 403:
            if PTLogin(logged=False):
                hdr['Cookie'] = get_cookies()
                list_html = utils._getHtml(url=url, referer=site.url, headers=hdr)
    name = '[COLOR hotpink]Sort Categories: [/COLOR][COLOR orange][{0}][/COLOR]'.format(get_sort_by(url=url))
    site.add_dir(name=name, url=url, mode='PTSet_sort_by_other')
    if url.find('?mode') > 0:
        match_cat = re.compile(pattern='<a class="item" href="([^"]+)" title="([^"]+)".*? src="([^"]+)".*?<div class="videos">([^"]+)</div>.*?<div class="rating positive">\s+([\d%]+)\s+</div>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
    else:
        cat_block = re.compile(pattern='<span class="icon type-video">(.*?)<div class="footer-margin">', flags=re.DOTALL | re.IGNORECASE).search(string=list_html).group(1)
        match_cat = re.compile(pattern='<a class="item" href="([^"]+)" title="([^"]+)".*? src="([^"]+)".*?<div class="videos">([^"]+)</div>.*?<div class="rating positive">\s+([\d%]+)\s+</div>', flags=re.DOTALL | re.IGNORECASE).findall(string=cat_block)
    for cat_page, name, img, videos, rating in match_cat:
        cat_page += lengthChoices[ptlength]
        cat_page += '?mode=async&function=get_block&block_id=list_videos_common_videos_list&sort_by=post_date&from=1'
        site.add_dir2(name='{0}[COLOR deeppink] {1}[/COLOR]'.format(name, videos), url=cat_page, mode='PTList', iconimage=resolve_img(img=img), page=1, desc='rating: ' + rating)
    utils.eod()


@site.register()
def PTSearch(url, keyword=None):
    searchUrl = url
    if not keyword:
        site.search_dir(url=url, mode='PTSearch')
    else:
        searchUrl += keyword.replace(' ', '%20')
        searchUrl += '/latest-updates/'
        searchUrl += lengthChoices[ptlength]
        if url.find('models') > 0:
            PTModels(url=searchUrl, page=1)
        else:
            ptlist = PTList(url=searchUrl, page=1)
            if not ptlist:
                utils.eod()


@site.register()
def PTLogin(logged=True):
    success = False
    ptlogged = utils.addon.getSetting(id='ptlogged')
    if not logged:
        ptlogged = False
        utils.addon.setSetting(id='ptlogged', value='false')

    if not ptlogged or 'false' in ptlogged:
        ptuser = utils.addon.getSetting(id='ptuser') if utils.addon.getSetting(id='ptuser') else ''
        ptpass = utils.addon.getSetting(id='ptpass') if utils.addon.getSetting(id='ptpass') else ''
        if ptuser == '':
            ptuser = getinput(default=ptuser, heading='Input your Porntrex username')
            ptpass = getinput(default=ptpass, heading='Input your Porntrex password', hidden=True)

        loginurl = '{0}ajax-login/'.format(site.url)
        postRequest = {'action': 'login',
                       'email_link': '{0}email/'.format(site.url),
                       'format': 'json',
                       'mode': 'async',
                       'pass': ptpass,
                       'remember_me': '1',
                       'username': ptuser}
        response = utils._postHtml(url=loginurl, form_data=postRequest)
        if 'success' in response.lower():
            utils.addon.setSetting(id='ptlogged', value='true')
            utils.addon.setSetting(id='ptuser', value=ptuser)
            utils.addon.setSetting(id='ptpass', value=ptpass)
            success = True
        else:
            utils.notify(header='Failure logging in', msg='Failure, please check your username or password')
            utils.addon.setSetting(id='ptuser', value='')
            utils.addon.setSetting(id='ptpass', value='')
            success = False
    elif ptlogged:
        clear = utils.selector(dialog_name='Clear stored user & password?', select_from=['Yes', 'No'])
        if clear:
            if clear == 'Yes':
                utils.addon.setSetting(id='ptuser', value='')
                utils.addon.setSetting(id='ptpass', value='')
            utils.addon.setSetting(id='ptlogged', value='false')
            utils._getHtml(url=site.url + 'logout/')
            xbmc.executebuiltin(function='Container.Update(' + utils.addon_sys + '?mode=' + site.name + '.PTMain' + ')')
    if logged:
        xbmc.executebuiltin(function='Container.Refresh')
    else:
        return success


@site.register()
#section: members, friends, members_friends
def PTMembers(url, page=1, onelist=None):
    global list_html
    if onelist:
        url = strip_end(text=url, suffix='=' + str(1)) + '=' + str(page)
    section = get_section_from_url(url=url)
    hdr = dict(utils.base_hdrs)
    hdr['Cookie'] = get_cookies()
    match_members = None
    try:
        list_html = utils._getHtml(url=url, referer=site.url, headers=hdr, error='raise')
    except urllib_error.HTTPError as e:
        if e.code == 403:
            if PTLogin(logged=False):
                hdr['Cookie'] = get_cookies()
                list_html = utils._getHtml(url=url, referer=site.url, headers=hdr)
    if page == 1:
        if section == 'members':
            name = '[COLOR hotpink]Sort Members: [/COLOR][COLOR orange][{0}][/COLOR]'.format(get_sort_by(url=url))
            site.add_dir2(name=name, url=url, mode='PTSet_sort_by_other', desc=set_trim_url(url=url))
    if section:
        if url.find('?mode') > 0 and section == 'members':
            match_members = re.compile(pattern='<div class="item.*?"><a href="([^"]+)" title="([^"]+)">.*? data-original="([^"]+)".*?<div class="added"><em>([^"]+)</em></div>.*?<div class="subscribe-block">.*?<a href="([^"]+)" class="button"', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
        elif url.find('?mode') > 0:
            match_members = re.compile(pattern='<div class="item.*?"><a href="([^"]+)" title="([^"]+)">.*? data-original="([^"]+)"', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
        elif section == 'members':
            cat_block = re.compile(pattern='<div id="list_members_members"(.*?)</div></div></div>', flags=re.DOTALL | re.IGNORECASE).search(string=list_html).group(1)
            match_members = re.compile(pattern='<div class="item.*?"><a href="([^"]+)" title="([^"]+)">.*? data-original="([^"]+)".*?<div class="added"><em>([^"]+)</em></div>.*?<div class="subscribe-block">.*?<a href="([^"]+)" class="button"', flags=re.DOTALL | re.IGNORECASE).findall(string=cat_block)
        elif section == 'friends':
            cat_block = re.compile(pattern='<div id="list_members_my_friends"(.*?)<div class="footer-margin">', flags=re.DOTALL | re.IGNORECASE).search(string=list_html).group(1)
            match_members = re.compile(pattern='<div class="item.*?"><a href="([^"]+)" title="([^"]+)">.*? data-original="([^"]+)"', flags=re.DOTALL | re.IGNORECASE).findall(string=cat_block)
        elif section == 'members_friends':
            cat_block = re.compile(pattern='<div id="list_members_friends"(.*?)<div class="footer-margin">', flags=re.DOTALL | re.IGNORECASE).search(list_html).group(1)
            match_members = re.compile(pattern='<div class="item.*?"><a href="([^"]+)" title="([^"]+)">.*? data-original="([^"]+)"', flags=re.DOTALL | re.IGNORECASE).findall(string=cat_block)
        if section == 'members':
            for mb_page, name, img, added, subscribe in match_members:
                contextmenu = [('[COLOR hotpink]GetInfo Member[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTGetInfoMember&url={2}'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(mb_page))+')')]
                if subscribe == '#unsubscribe':
                    name = '[COLOR blue]' + name + '[/COLOR]'
                    contextmenu.append(('[COLOR hotpink]Unsubscribe Member[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTContextMenu&url={2}&fav=unsubscribe_member'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(mb_page))+')'))
                else:
                    name = '[COLOR white]' + name + '[/COLOR]'
                    contextmenu.append(('[COLOR hotpink]Subscribe Member[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTContextMenu&url={2}&fav=subscribe_member'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(mb_page))+')'))
                mb_page += 'favourites/videos/?mode=async&function=get_block&block_id=list_videos_favourite_videos&fav_type=0&playlist_id=0&sort_by=&from_fav_videos=1'
                if ptrange == 'No':
                    site.add_dir2(name=name, url=mb_page, page=1, mode='PTList', iconimage=resolve_img(img=img), desc='added: ' + added, contextm=contextmenu)
                else:
                    site.add_dir2(name=name, url=mb_page, page=1, mode='PTListSort', onelist=4, iconimage=resolve_img(img=img), desc='added: ' + added, contextm=contextmenu)

        elif section == 'friends' or section == 'members_friends':
            for mbo_page, name, img in match_members:
                mbo_page += 'favourites/videos/?mode=async&function=get_block&block_id=list_videos_favourite_videos&fav_type=0&playlist_id=0&sort_by=&from_fav_videos=1'
                contextmenu = [('[COLOR hotpink]GetInfo Member[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTGetInfoMember&url={2}'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(mbo_page))+')')]
                if ptrange == 'No':
                    site.add_dir2(name=name, url=mbo_page, page=1, mode='PTList', iconimage=resolve_img(img=img), contextm=contextmenu)
                else:
                    site.add_dir2(name=name, url=mbo_page, page=1, mode='PTListSort', onelist=4, iconimage=resolve_img(img=img), contextm=contextmenu)

    if not onelist:
        page_list(url=url, page=page, mode='PTMembers', content=list_html, section=section)
        utils.eod()


@site.register()
def PTPlaylists(url, page=1, onelist=None):
    print('url_PTPlaylists ' + url)
    global list_html
    if onelist:
        url = strip_end(text=url, suffix='=' + str(1)) + '=' + str(page)
    hdr = dict(utils.base_hdrs)
    hdr['Cookie'] = get_cookies()
    try:
        list_html = utils._getHtml(url=url, referer=site.url, headers=hdr, error='raise')
    except urllib_error.HTTPError as e:
        if e.code == 403:
            if PTLogin(logged=False):
                hdr['Cookie'] = get_cookies()
                list_html = utils._getHtml(url=url, referer=site.url, headers=hdr)
    if '/members/' not in url and '/my/' not in url:
        if page == 1:
            name = '[COLOR hotpink]Sort Playlists: [/COLOR][COLOR orange][{0}][/COLOR]'.format(get_sort_by(url=url))
            site.add_dir2(name=name, url=url, mode='PTSet_sort_by_other', desc=set_trim_url(url=url))
    if '/members/' in url:
        match_playlists = re.compile(pattern='<a href="([^"]+)" title="([^"]+)".*?data-original="([^"]+)".*?<div class="added"><em>([^"]+) ago</em></div>\s+<div class="rating positive">\s+([\d%]+)\s+</div>.*?<div class="viewsthumb">([^"]+) views</div>\s+<div class="totalplaylist">(\d+)', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
        match_playlists.reverse()
    elif url.find('?mode') > 0:
        match_playlists = re.compile(pattern='<a href="([^"]+)" title="([^"]+)".*?data-original="([^"]+)".*?<div class="added"><em>([^"]+) ago</em></div>\s+<div class="rating positive">\s+([\d%]+)\s+</div>.*?<div class="viewsthumb">([^"]+) views</div>\s+<div class="totalplaylist">(\d+)', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
    else:
        pl_block = re.compile(pattern='<div class="list-playlists">(.*?)<div class="footer-margin">', flags=re.DOTALL | re.IGNORECASE).search(string=list_html).group(1)
        match_playlists = re.compile(pattern='<a href="([^"]+)" title="([^"]+)".*?data-original="([^"]+)".*?<div class="added"><em>([^"]+) ago</em></div>\s+<div class="rating positive">\s+([\d%]+)\s+</div>.*?<div class="viewsthumb">([^"]+) views</div>\s+<div class="totalplaylist">(\d+)', flags=re.DOTALL | re.IGNORECASE).findall(string=pl_block)
    for pl_page, name, img, added, rating, views, count in match_playlists:
        views = str(utils.cleantext(text=views)).replace(' ', '')
        desc = 'views: ' + views + '\n' + 'added: ' + added + '\n' + 'rating: ' + rating
        contextmenu = []
        contextmenu.append(('[COLOR hotpink]GetInfo Playlist[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTGetInfoPlaylist&name={2}&url={3}'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(name), urllib_parse.quote_plus(pl_page))+')'))
        if '/my/playlists/' not in url:
            contextmenu.append(('[COLOR hotpink]Subscribe Playlist[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTContextMenu&url={2}&fav=subscribe_playlist'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(pl_page))+')'))
            contextmenu.append(('[COLOR hotpink]Unsubscribe Playlist[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTContextMenu&url={2}&fav=unsubscribe_playlist'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(pl_page))+')'))
        site.add_dir2(name=name + '[COLOR hotpink] ({0})[/COLOR]'.format(count), url=pl_page, page=1, mode='PTPlaylist', iconimage=resolve_img(img=img), contextm=contextmenu, desc=desc)
    if not onelist:
        page_list(url=url, page=page, mode='PTPlaylists', content=list_html)
        utils.eod()


@site.register()
def PTPlaylist(url, page=1):
    member_url_check, _ = get_member_url_check_name_url(url=url)
    m_my = ''
    if '/my/' in member_url_check:
        m_my = 'my_'
    url_pl = '{0}favourites/videos/?mode=async&function=get_block&block_id=list_videos_{1}favourite_videos&fav_type=10&playlist_id={2}&sort_by=&from_{1}fav_videos={3}'.format(member_url_check, m_my, str(url.split('/')[4]), str(page))
    if ptrange == 'No':
        ptlist = PTList(url=url_pl, page=1)
    else:
        ptlist = PTListSort(url=url_pl, page=1, onelist=4)
    if not ptlist:
        utils.eod()


@site.register()
def PTModels(url, page=1, onelist=None):
    if onelist:
        url = url.replace('/1/', '/' + str(page) + '/')
        url = strip_end(text=url, suffix='=' + str(1)) + '=' + str(page)
    hdr = dict(utils.base_hdrs)
    hdr['Cookie'] = get_cookies()
    try:
        list_html = utils._getHtml(url=url, referer=site.url, headers=hdr, error='raise')
    except urllib_error.HTTPError as e:
        if e.code == 403:
            if PTLogin(logged=False):
                hdr['Cookie'] = get_cookies()
                list_html = utils._getHtml(url=url, referer=site.url, headers=hdr)
    if page == 1:
        if '/search/models/' not in url:
            site.add_dir(name='[COLOR hotpink]Sort Models Alpha: [/COLOR][COLOR orange][{0}][/COLOR]'.format(get_sort_by(url=url)), url=url, mode='PTSet_sortby_model_alpha')
            site.add_dir2(name='[COLOR hotpink]Sort Models: [/COLOR][COLOR orange][{0}][/COLOR]'.format(get_sort_by(url=url)), url=url, mode='PTSet_sort_by_other', desc=set_trim_url(url=url))
        site.add_dir(name='[COLOR hotpink]Search Models[/COLOR]', url='{0}search/models'.format(site.url), mode='PTSearch')
    match_models = re.compile(pattern='<a class="item" href="([^"]+)" title="([^"]+)".*? src="([^"]+)".*?<div class="videos">([\d]+) videos</div>\s+<div class="rating positive">\s+([\d%]+)\s+</div>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
    for md_page, name, img, count, rating in match_models:
        name += '[COLOR hotpink] ({0})[/COLOR]'.format(count)
        md_page += lengthChoices[ptlength]
        md_page_url = '{0}?mode=async&function=get_block&block_id=list_videos_common_videos_list_norm&sort_by=post_date&from4=1'.format(md_page)
        id_nr = resolve_img(img=img).split('/')[5] if 'no-image-model' not in img else None
        desc = 'rating: ' + rating
        if ptlogged and id:
            contextmenu = [('[COLOR hotpink]GetInfo Model[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTGetInfoModel&name={2}&url={3}'.format(utils.addon_sys, site.name, name, urllib_parse.quote_plus(md_page))+')'),
                           ('[COLOR deeppink]Subscribe Model[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTContextMenu&url={2}&fav=subscribe_model&filtered={3}'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(md_page), str(id_nr))+')'),
                           ('[COLOR deeppink]Unsubscribe Model[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTContextMenu&url={2}&fav=unsubscribe_model&filtered={3}'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(md_page), str(id_nr))+')')]
            site.add_dir2(name=name, url=md_page_url, page=1, mode='PTList', iconimage=resolve_img(img=img), desc=desc, contextm=contextmenu)
        else:
            site.add_dir2(name=name, url=md_page_url, page=1, mode='PTList', iconimage=resolve_img(img=img), desc=desc)
    if not onelist:
        page_list(url=url, page=page, mode='PTModels', content=list_html)
        utils.eod()


@site.register()
def PTSubscriptions(url, page=1, onelist=None):
    global list_html
    if onelist:
        url = strip_end(text=url, suffix='=' + str(1)) + '=' + str(page)
    hdr = dict(utils.base_hdrs)
    hdr['Cookie'] = get_cookies()
    try:
        list_html = utils._getHtml(url=url, referer=site.url, headers=hdr, error='raise')
    except urllib_error.HTTPError as e:
        if e.code == 403:
            if PTLogin(logged=False):
                hdr['Cookie'] = get_cookies()
                list_html = utils._getHtml(url=url, referer=site.url, headers=hdr)
    match = re.compile(pattern='<div class="item friend new">\s+<a href="([^"]+)" title="([^"]+)">.*?data-original="([^"]+)"', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
    for cat_page, name, img in match:
        if '/members/' in cat_page:
            contextmenu = [('[COLOR hotpink]GetInfo Member[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTGetInfoMember&url={2}'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(cat_page))+')'),
                           ('[COLOR hotpink]Unsubscribe Member[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTContextMenu&url={2}&fav=unsubscribe_member'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(cat_page))+')')]
            site.add_dir2(name=name, url='{0}favourites/videos/?mode=async&function=get_block&block_id=list_videos_favourite_videos&fav_type=0&playlist_id=0&sort_by=&from_fav_videos=1'.format(cat_page), page=1, mode='PTList', iconimage=resolve_img(img=img), contextm=contextmenu, desc=set_trim_url(url=cat_page))
        elif '/playlists/' in cat_page:
            contextmenu = [('[COLOR hotpink]GetInfo Playlist[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTGetInfoPlaylist&name={2}&url={3}'.format(utils.addon_sys, site.name, name, urllib_parse.quote_plus(cat_page))+')'),
                           ('[COLOR hotpink]Unsubscribe Playlist[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTContextMenu&url={2}&fav=unsubscribe_playlist'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(cat_page))+')')]
            site.add_dir2(name=name, url=cat_page, page=1, mode='PTPlaylist', contextm=contextmenu, desc=set_trim_url(url=cat_page))
        elif '/models/' in cat_page:
            cat_page += lengthChoices[ptlength]
            try:
                id_nr = resolve_img(img=img).split('/')[5]
            except:
                id_nr = None
            contextmenu = [('[COLOR hotpink]GetInfo Model[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTGetInfoModel&name={2}&url={3}'.format(utils.addon_sys, site.name, name, urllib_parse.quote_plus(cat_page))+')'),
                           ('[COLOR deeppink]Unsubscribe Model[/COLOR]', 'RunPlugin('+'{0}?mode={1}.PTContextMenu&url={2}&fav=unsubscribe_model&filtered={3}'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(cat_page), str(id_nr))+')')]
            site.add_dir2(name=name, url='{0}?mode=async&function=get_block&block_id=list_videos_common_videos_list_norm&sort_by=post_date&from4=1'.format(cat_page), page=1, mode='PTList', iconimage=resolve_img(img=img), contextm=contextmenu, desc=set_trim_url(url=cat_page))
    if not onelist:
        page_list(url=url, page=page, mode='PTSubscriptions', content=list_html)
        utils.eod()


@site.register()
def PTSearchFilterCategory(url, keyword=None):
    hdr = dict(utils.base_hdrs)
    hdr['Cookie'] = get_cookies()
    searchUrl = url
    search_sort = 'post_date'
    category = utils.addon.getSetting(id='pt_category')
    if not keyword:
        site.search_dir(url=searchUrl, mode='PTSearchFilterCategory')
    else:
        title = keyword.replace('+', '-')
        searchUrl = url + '/' + title + '/latest-updates/'
        if '-' in title:
            search_sort = 'relevance'
            searchUrl = url + '/' + title + '/'
        searchUrl += lengthChoices[ptlength]
    try:
        list_html = utils._getHtml(url=searchUrl, referer=site.url, headers=hdr)
    except:
        return None
    filter_category = {}
    match_filter = re.compile(pattern='<label class="text" for="category_filter_(\d+)">([^"]+)</label>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
    for int_category, name in match_filter:
        if category:
            int_category = category + ',' + int_category
        filter_category[name] = int_category
    selected_filter_category = utils.selector(dialog_name='Pick a category to look up videos', select_from=filter_category, show_on_one=True)
    if not selected_filter_category:
        return
    utils.addon.setSetting(id='pt_category', value=selected_filter_category)
    ptlist = PTList(url='{0}?mode=async&function=get_block&block_id=list_videos_videos&q={1}&category_ids={2}&sort_by={3}&from=1'.format(searchUrl, keyword, selected_filter_category, search_sort), page=1)
    if not ptlist:
        utils.eod()


@site.register()
def PTContextMenu(url, fav, filtered=None):
    hdr = dict(utils.base_hdrs)
    hdr['Cookie'] = get_cookies()
    id_nr = url.split('/')[4]
    json_url = None
    msg_notify = None
    if fav == 'add_fav':
        json_url = '{0}?mode=async&format=json&action=add_to_favourites&video_id={1}&album_id=&fav_type=0&playlist_id=0'.format(url, id_nr)
        msg_notify = 'Added to Favorites'
    elif fav == 'del_fav':
        json_url = '{0}?mode=async&format=json&action=delete_from_favourites&video_id={1}&album_id=&fav_type=0&playlist_id=0'.format(url, id_nr)
        msg_notify = 'Deleted from Favorites'
    elif fav == 'add_w_later':
        json_url = '{0}?mode=async&format=json&action=add_to_favourites&video_id={1}&album_id=&fav_type=1&playlist_id=0'.format(url, id_nr)
        msg_notify = 'Added to Watch Later'
    elif fav == 'del_w_later':
        json_url = '{0}?mode=async&format=json&action=delete_from_favourites&video_id={1}&album_id=&fav_type=1&playlist_id=0'.format(url, id_nr)
        msg_notify = 'Deleted from Watch Later'
    elif fav == 'subscribe_member':
        json_url = '{0}?mode=async&format=json&action=subscribe&subscribe_user_id={1}'.format(url, id_nr)
        msg_notify = 'Subscribed Member'
    elif fav == 'unsubscribe_member':
        json_url = '{0}?mode=async&format=json&action=unsubscribe&unsubscribe_user_id={1}'.format(url, id_nr)
        msg_notify = 'Unsubscribed Member'
    elif fav == 'subscribe_playlist':
        blnSubscription = get_subscription(url=url)
        if blnSubscription:
            utils.notify(msg='Playlist has been Subscribed')
        else:
            json_url = '{0}?mode=async&format=json&action=subscribe&subscribe_playlist_id={1}'.format(url, id_nr)
            msg_notify = 'Subscribed Playlist'
    elif fav == 'unsubscribe_playlist':
        json_url = '{0}?mode=async&format=json&action=unsubscribe&unsubscribe_playlist_id={1}'.format(url, id_nr)
        msg_notify = 'Unsubscribed Playlist'
    elif fav == 'subscribe_model':
        blnSubscription = get_subscription(url=url)
        if blnSubscription:
            utils.notify(msg='Model has been Subscribed')
        else:
            json_url = '{0}?mode=async&format=json&action=subscribe&subscribe_model_id={1}'.format(url, filtered)
            msg_notify = 'Subscribed Model'
    elif fav == 'unsubscribe_model':
        json_url = '{0}?mode=async&format=json&action=unsubscribe&unsubscribe_model_id={1}'.format(url, filtered)
        msg_notify = 'Unsubscribed Model'
    elif fav == 'del_from_playlist':
        json_url = '{0}?mode=async&format=json&action=delete_from_favourites&video_id={1}&album_id=&fav_type=10&playlist_id={2}'.format(url, url.split('/')[4], filtered)
        msg_notify = 'Deleted from Playlist'
    if json_url and msg_notify:
        resp = utils._getHtml(url=json_url, referer=site.url, headers=hdr)
        if 'success' in resp:
            fav_check_lst = ['add_fav', 'del_fav', 'add_w_later', 'del_w_later']
            if any(s == fav for s in fav_check_lst):
                fav_total = re.findall(pattern='"favourites_total":(\d+)', string=resp)[0]
                fav_type = re.findall(pattern='"favourites_type":(\d+)', string=resp)[0]
                if fav_total and fav_type:
                    msg_notify += ' (' + fav_type + ',' + fav_total + ')'
            fav_check_lst = ['del_from_playlist']
            if any(s == fav for s in fav_check_lst):
                fav_total = re.findall(pattern='"favourites_total":(\d+)', string=resp)[0]
                fav_playlist = re.findall(pattern='"favourites_playlist":(\d+)', string=resp)[0]
                if fav_total and fav_playlist:
                    msg_notify += ' (' + fav_playlist + ',' + fav_total + ')'
            utils.notify(msg=msg_notify, duration=10)
            fav_check_lst = ['del_from_playlist']
            if any(s == fav for s in fav_check_lst):
                xbmc.executebuiltin(function='Container.Refresh')
        else:
            msg = re.findall(pattern='message":"([^"]+)"', string=resp)[0]
            utils.notify(msg=msg)
        return


@site.register()
def PTCheck_tags(url):
    hdr = dict(utils.base_hdrs)
    hdr['Cookie'] = get_cookies()
    try:
        list_html = utils._getHtml(url=url, referer=site.url, headers=hdr)
    except:
        return None
    tags = {}
    match_tags = re.compile(pattern='<a href="([^"]+tags[^"]+)">([^<]+)</a>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
    if match_tags:
        for url_tag, tag in match_tags:
            tag = tag.strip()
            if tag.startswith('-'):
                continue
            tags[tag] = url_tag
        selected_tag = utils.selector(dialog_name='Pick a tag to look up videos', select_from=tags, show_on_one=True)
        if not selected_tag:
            return
        xbmc.executebuiltin(function='Container.Update('+'{0}?mode={1}.PTList&url={2}&page=1'.format(utils.addon_sys, site.name, urllib_parse.quote_plus('{0}?mode=async&function=get_block&block_id=list_videos_common_videos_list_norm&sort_by=post_date&from4=1'.format(selected_tag)))+')')
    else:
        utils.notify(header='Notify', msg='No tags found at this video')
        return


@site.register()
def PTCheck_models(url):
    hdr = dict(utils.base_hdrs)
    hdr['Cookie'] = get_cookies()
    try:
        list_html = utils._getHtml(url=url, referer=site.url, headers=hdr)
    except:
        return None
    models = {}
    match_models = re.compile(pattern='<a href="([^"]+)"><i class="fa fa-star"></i> ([^"]+)</a>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
    if match_models:
        for url_md, model in match_models:
            model = model.strip()
            list_md_html = utils._getHtml(url=url_md)
            blnSubscription = get_subscription(url=url_md, list_html=list_md_html)
            if blnSubscription:
                model = '[COLOR blue]' + model + '[/COLOR]'
            models[model] = url_md
        selected_model = utils.selector(dialog_name='Pick a model to look up videos', select_from=models, show_on_one=True)
        if not selected_model:
            return
        xbmc.executebuiltin(function='Container.Update('+'{0}?mode={1}.PTList&url={2}&page=1'.format(utils.addon_sys, site.name, urllib_parse.quote_plus('{0}?mode=async&function=get_block&block_id=list_videos_common_videos_list_norm&sort_by=post_date&from4=1'.format(selected_model)))+')')
    else:
        utils.notify(header='Notify', msg='No models found at this video')
        return


@site.register()
def PTCheck_playlists(url, fav, filtered=None):
    msg_notify = None
    hdr = dict(utils.base_hdrs)
    hdr['Cookie'] = get_cookies()
    try:
        list_html = utils._getHtml(url=site.url + 'select-playlist/', referer=site.url, headers=hdr)
    except:
        return None
    id_nr = url.split('/')[4]
    playlists = {}
    match_playlists = re.compile(pattern='<input type="radio" class="radio" name="playlist_id" value="(\d+)"/>\s+<span>\s+([^"]+)\s+-\s+[^"]+\s+-\s+(\d+) videos\s+</span>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
    if match_playlists:
        for id_pl, playlist, count in match_playlists:
            playlist = utils.cleantext(text=playlist) + ' (' + count + ')'
            playlist = playlist.strip()
            playlists[playlist] = id_pl
        selected_playlist = utils.selector(dialog_name='Pick a playlist to look up videos', select_from=playlists, show_on_one=True)
        if not selected_playlist:
            return
        for name, value in playlists.items():
            if value == selected_playlist:
                msg_notify = name
                continue
        if fav == 'add_to_playlist':
            json_url = '{0}?mode=async&format=json&action=add_to_favourites&video_id={1}&album_id=&fav_type=10&playlist_id={2}'.format(url, id_nr, selected_playlist)
            header_notify = 'Added to Playlist'
        elif fav == 'move_to_playlist':
            json_url = '{0}my/favourites/videos/?mode=async&format=json&action=delete_from_favourites&fav_type=10&playlist_id={1}&function=get_block&block_id=list_videos_my_favourite_videos&move_to_playlist_id={2}&delete%5B%5D={3}'.format(site.url, filtered, selected_playlist, id_nr)
            header_notify = 'Moved to Playlist'
        else:
            json_url = None
            header_notify = None
        resp = utils._getHtml(url=json_url, referer=site.url, headers=hdr)
        if 'success' in resp:
            fav_check_lst = ['add_to_playlist']
            if any(s == fav for s in fav_check_lst):
                fav_total = re.findall(pattern='"favourites_total":(\d+)', string=resp)[0]
                fav_playlist = re.findall(pattern='"favourites_playlist":(\d+)', string=resp)[0]
                if fav_total and fav_playlist:
                    msg_notify += ' (' + fav_playlist + ',' + fav_total + ')'
            utils.notify(header=header_notify, msg=msg_notify, duration=10)
        else:
            msg = re.findall(pattern='message":"([^"]+)"', string=resp)[0]
            utils.notify(msg=msg)
        return
    else:
        utils.notify(header='Notify', msg='No playlists found')
        return


@site.register()
def PTCheck_member(url):
    hdr = dict(utils.base_hdrs)
    hdr['Cookie'] = get_cookies()
    try:
        list_html = utils._getHtml(url=url, referer=site.url, headers=hdr)
    except:
        return None
    member_url_check, member_name = get_member_url_check_name_url(url=url, list_html=list_html)
    member_list = {member_name: member_url_check}
    selected_mb = utils.selector(dialog_name='Pick a member to look up videos', select_from=member_list, show_on_one=True)
    if not selected_mb:
        return
    m_my = ''
    if '/my/' in url:
        m_my = 'my_'
    upl_url = '{0}videos/?mode=async&function=get_block&block_id=list_videos_{1}uploaded_videos&sort_by=&from_{1}uploaded_videos=1'.format(member_url_check, m_my)
    xbmc.executebuiltin(function='Container.Update('+'{0}?mode={1}.PTList&url={2}&page=1'.format(utils.addon_sys, site.name, urllib_parse.quote_plus(upl_url))+')')


@site.register()
def PTSet_sort_by_videos(url):
    hdr = dict(utils.base_hdrs)
    hdr['Cookie'] = get_cookies()
    try:
        list_html = utils._getHtml(url=url, referer=site.url, headers=hdr)
    except:
        return None
    section = get_section_from_url(url=url)
    nextFolder = get_next_folder_from_url(url=url, folder=section, int=1)
    if section and nextFolder:
        url_nextFolder = site.url + section + '/' + nextFolder + '/'
    else:
        url_nextFolder = site.url
    match = re.compile(pattern='<div class="sort-holder">(.*?)<div class="porntrex-box">', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
    match1 = re.compile(pattern='<li><a href="([^"]+)">([^"]+)</a></li>', flags=re.DOTALL | re.IGNORECASE).findall(string=match[0])
    match2 = re.compile(pattern='<a href="([^"]+)"><strong>([^"]+)</strong></a>', flags=re.DOTALL | re.IGNORECASE).findall(string=match[0])
    act_sort = re.compile(pattern='<div class="headline" data="([^"]+)"><h1>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)[0]
    a_sort = re.compile(pattern='<div class="sort"><span class="icon type-sort"></span><strong>([^"]+)</strong>', flags=re.DOTALL | re.IGNORECASE).findall(string=match[0])
    a_sort2 = re.compile(pattern='<li class="item\s+active"><a href="[^"]+"><strong>([^"]+)</strong>', flags=re.DOTALL | re.IGNORECASE).findall(string=match[0])[0]
    ahd_sort = re.compile(pattern='<div class="hd-sort.*?href="([^"]+)" class="active">([^"]+)</a>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
    hd_sort = re.compile(pattern='<div class="hd-sort.*?href="([^"]+)" >([^"]+)</a>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
    if a_sort[-1] == 'Length':
        a_sort[-1] = 'All'
    if act_sort == 'post_date':
        a_sort2 = 'Latest'
    sort_by_list = {}
    for cat_url, name in ahd_sort:
        if name == 'All':
            name = '[COLOR hotpink]All HD[/COLOR]'
        name = '[COLOR hotpink]' + name + '[/COLOR]'
        sort_by_list[name] = None
    for cat_url, name in hd_sort:
        if name == 'All':
            name = '[COLOR white]All HD[/COLOR]'
        name = '[COLOR white]' + name + '[/COLOR]'
        sort_by_list[name] = cat_url
    for cat_url, name in match2:
        if a_sort2 == name:
            name = '[COLOR hotpink]' + name + '[/COLOR]'
            cat_url = None
        if '[COLOR hotpink]' not in name:
            name = '[COLOR white]' + name + '[/COLOR]'
        sort_by_list[name] = cat_url
    for cat_url, name in match1:
        for v_sort in a_sort:
            if str(v_sort) == name:
                if name == 'All':
                    name = '[COLOR hotpink]All Length[/COLOR]'
                name = '[COLOR hotpink]' + name + '[/COLOR]'
                cat_url = None
        if '[COLOR hotpink]' not in name:
            if name == 'All':
                name = '[COLOR white]All Length[/COLOR]'
            name = '[COLOR white]' + name + '[/COLOR]'
        sort_by_list[name] = cat_url
    match_list = {
        'Most Viewed This Week': url_nextFolder + 'most-popular/weekly/',
        'Top Rated This Week': url_nextFolder + 'top-rated/weekly/',
        'Trending': url_nextFolder + 'last-viewed/',
    }
    for name, cat_url in match_list.items():
        if cat_url == url:
            sort_by_list['[COLOR hotpink]' + name + '[/COLOR]'] = None
        else:
            sort_by_list['[COLOR white]' + name + '[/COLOR]'] = cat_url
    selected_sort = utils.selector(dialog_name='Pick a sort option', select_from=sort_by_list)
    if not selected_sort:
        return None
    ptlist = PTList(url=selected_sort, page=1)
    if not ptlist:
        utils.eod()


@site.register()
def PTSet_sort_by_private_videos(url):
    url_root = url.split('?mode')[0]
    sort_by_list = {}
    for name, cat_url in private_videoChoices.items():
        if cat_url in url:
            sort_by_list['[COLOR hotpink]' + name + '[/COLOR]'] = None
        else:
            sort_by_list['[COLOR white]' + name + '[/COLOR]'] = cat_url
    selected_private = utils.selector(dialog_name='Select', select_from=sort_by_list)
    url_prv = '{0}?mode=async&function=get_block&block_id=list_videos_common_videos_list_norm&sort_by={1}&from4=1'.format(url_root, selected_private)
    if not selected_private:
        return None
    ptlist = PTList(url=url_prv, page=1)
    if not ptlist:
        utils.eod()


@site.register()
def PTSet_Listsort_by_videos(url, page, onelist):
    sort_by_list = {}
    for name, cat_url in sortChoices.items():
        if cat_url == ptrangesort:
            sort_by_list['[COLOR hotpink]' + name + '[/COLOR]'] = None
        else:
            sort_by_list['[COLOR white]' + name + '[/COLOR]'] = cat_url
    selected_plist = utils.selector(dialog_name='Select', select_from=sort_by_list)
    if not selected_plist:
        return None
    utils.addon.setSetting(id='ptrangesort', value=selected_plist)
    ptlist = PTListSort(url=url, page=page, onelist=onelist)
    if not ptlist:
        utils.eod()


@site.register()
def PTSet_sort_by_videos_search(url):
    hdr = dict(utils.base_hdrs)
    hdr['Cookie'] = get_cookies()
    try:
        list_html = utils._getHtml(url=url, referer=site.url, headers=hdr)
    except:
        return None
    command_check_lst = ['Most Favourited', 'Most Commented', 'All Time', 'This Month', 'This Week', 'Today']
    command_check_lst2 = ['0~10 min', '10~30 min', '30+ min']
    match = re.compile(pattern='<div class="sort-holder search">(.*?)<div class="porntrex-box">', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
    match1 = re.compile(pattern='<li><a href="([^"]+)">([^"]+)</a></li>', flags=re.DOTALL | re.IGNORECASE).findall(string=match[0])
    match2 = re.compile(pattern='<a href="([^"]+)"><strong>([^"]+)</strong></a>', flags=re.DOTALL | re.IGNORECASE).findall(string=match[0])
    a_sort = re.compile(pattern='<div class="sort"><span class="icon type-sort"></span><strong>([^"]+)</strong>', flags=re.DOTALL | re.IGNORECASE).findall(string=match[0])
    a_sort2 = re.compile(pattern='<li class="item\s+active"><a href="[^"]+"><strong>([^"]+)</strong>', flags=re.DOTALL | re.IGNORECASE).findall(string=match[0])[0]
    if 'latest-updates' not in url and a_sort2 == 'Latest':
        a_sort2 = 'Most Relevant'
    if a_sort[-1] == 'Length':
        a_sort[-1] = 'All'
    sort_by_list = {}
    for cat_url, name in match2:
        if name == 'Best':
            continue
        if a_sort2 == name:
            name = '[COLOR hotpink]' + name + '[/COLOR]'
            cat_url = None
        if '[COLOR hotpink]' not in name:
            name = '[COLOR white]' + name + '[/COLOR]'
        sort_by_list[name] = cat_url
    for cat_url, name in match1:
        if name in command_check_lst or a_sort2 == 'Most Relevant' and name in command_check_lst2:
            continue
        for v_sort in a_sort:
            if str(v_sort) == name:
                if name == 'All':
                    name = '[COLOR hotpink]All Length[/COLOR]'
                name = '[COLOR hotpink]' + name + '[/COLOR]'
                cat_url = None
        if '[COLOR hotpink]' not in name:
            if name == 'All':
                name = '[COLOR white]All Length[/COLOR]'
            name = '[COLOR white]' + name + '[/COLOR]'
        sort_by_list[name] = cat_url
    selected_search = utils.selector(dialog_name='Pick a sort option', select_from=sort_by_list)
    if not selected_search:
        return None
    category = utils.addon.getSetting(id='pt_category')
    ptlist = PTList(url=get_ajax_search_page1_url(url=selected_search, category=category), page=1)
    if not ptlist:
        utils.eod()


@site.register()
#section: members, playlists, models, categories
def PTSet_sort_by_other(url):
    hdr = dict(utils.base_hdrs)
    hdr['Cookie'] = get_cookies()
    try:
        list_html = utils._getHtml(url=url, referer=site.url, headers=hdr)
    except:
        return None
    section = get_section_from_url(url=url)
    global match1
    url_root = url.split('?mode')[0]
    if section:
        try:
            a_sort = re.compile(pattern='<div class="sort">\s+<span class="icon type-sort"></span>\s+<strong>([^"]+)</strong>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
            if section == 'members':
                match = re.compile(pattern='<ul id="list_members_members_sort_list">(.*?)</ul>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
                match1 = re.compile(pattern='<a data-action="ajax" data-container-id="list_members_members_sort_list" data-block-id="list_members_members" data-parameters="([^"]+)">([^"]+)</a>', flags=re.DOTALL | re.IGNORECASE).findall(string=match[0])
                a_sort = re.compile(pattern='<div class="sort"><span class="icon type-sort"></span><strong>([^"]+)</strong>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
            elif section == 'playlists':
                match = re.compile(pattern='<ul id="list_playlists_common_playlists_list_sort_list">(.*?)</ul>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
                match1 = re.compile(pattern='<a data-action="ajax" data-container-id="list_playlists_common_playlists_list_sort_list" data-block-id="list_playlists_common_playlists_list" data-parameters="([^"]+)">([^"]+)</a>', flags=re.DOTALL | re.IGNORECASE).findall(string=match[0])
            elif section == 'models':
                match = re.compile(pattern='<ul id="list_models_models_list_sort_list">(.*?)<div class="sort">', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
                match1 = re.compile(pattern='<a data-action="ajax" data-container-id="list_models_models_list_sort_list" data-block-id="list_models_models_list" data-parameters="([^"]+)">([^"]+)</a>', flags=re.DOTALL | re.IGNORECASE).findall(string=match[0])
            elif section == 'categories':
                match = re.compile(pattern='<ul id="list_categories_categories_list_sort_list">(.*?)</ul>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
                match1 = re.compile(pattern='<a data-action="ajax" data-container-id="list_categories_categories_list_sort_list" data-block-id="list_categories_categories_list" data-parameters="([^"]+)">([^"]+)</a>', flags=re.DOTALL | re.IGNORECASE).findall(string=match[0])
        except:
            return None
        sort_by_list = {}
        for name in a_sort:
            name = utils.cleantext(text=name)
            name = '[COLOR hotpink]' + name + '[/COLOR]'
            sort_by_list[name] = None
        for url_other, name in match1:
            name = utils.cleantext(text=name)
            name = '[COLOR white]' + name + '[/COLOR]'
            url_other = clean_url(text=url_other)
            if section == 'members':
                url_other = '{0}?mode=async&function=get_block&block_id=list_members_members&{1}&from_members=1'.format(url_root, url_other)
            elif section == 'playlists':
                url_other = '{0}?mode=async&function=get_block&block_id=list_playlists_common_playlists_list&{1}&from=1'.format(url_root, url_other)
            elif section == 'models':
                url_other = '{0}?mode=async&function=get_block&block_id=list_models_models_list&{1}&from=1'.format(url_root, url_other)
            elif section == 'categories':
                url_other = '{0}?mode=async&function=get_block&block_id=list_categories_categories_list&{1}&from=1'.format(url_root, url_other)
            sort_by_list[name] = url_other
        selected_other = utils.selector(dialog_name='Pick a sort option', select_from=sort_by_list)
        if not selected_other:
            return None
        for name, value in sort_by_list.items():
            if value == selected_other:
                if 'hotpink' not in value:
                    if section == 'members':
                        PTMembers(url=selected_other, page=1)
                    elif section == 'playlists':
                        PTPlaylists(url=selected_other, page=1)
                    elif section == 'models':
                        PTModels(url=selected_other, page=1)
                    elif section == 'categories':
                        PTCat(url=selected_other)


@site.register()
def PTSet_sortby_model_alpha(url):
    match = [[site.url + 'models/1/', 'All']]
    for x in range(ord('a'), ord('z')+1):
        match.insert(x, (site.url + 'models/' + chr(x) + '/', chr(x)))
    sort_by_list = {}
    for cat_url, name in match:
        sort_by_list[name] = cat_url
    selected_model_alpha = utils.selector(dialog_name='Pick a sort option', select_from=sort_by_list)
    if not selected_model_alpha:
        return None
    for name, value in sort_by_list.items():
        if value == selected_model_alpha:
            if name == 'All':
                sort_by_section = get_sort_by(url=url).split('&section')[0]
            else:
                sort_by_section = get_sort_by(url=url).split('&section')[0] + '&section=' + name.lower()
            PTModels(url='{0}?mode=async&function=get_block&block_id=list_models_models_list&sort_by={1}&from=1'.format(selected_model_alpha, str(sort_by_section)), page=1)


@site.register()
def PTGetInfoVideoTextBox(url, desc):
    hdr = dict(utils.base_hdrs)
    hdr['Cookie'] = get_cookies()
    try:
        list_html = utils._getHtml(url=url, referer=site.url, headers=hdr)
    except:
        return None
    _, member_name = get_member_url_check_name_url(url=url, list_html=list_html)
    try:
        cat_block_model = re.compile(pattern='<span class="title-item">Models:</span>(.*?)<span class="title-item">Categories:</span>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
        cat_block_cat = re.compile(pattern='<span class="title-item">Categories:</span>(.*?)<span class="title-item">Tags:</span>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
        cat_block_tags = re.compile(pattern='<span class="title-item">Tags:</span>(.*?)<span class="title-item">Description:</span>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
        cat_block_desc = re.compile(pattern='<span class="title-item">Description:</span>(.*?)</div>\s+</div>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
        match_model = re.compile(pattern='<a href="([^"]+)"><i class="fa fa-star"></i> ([^"]+)</a>', flags=re.DOTALL | re.IGNORECASE).findall(string=cat_block_model[0])
        match_cat = re.compile(pattern='<a class="js-cat" href="[^"]+">([^"]+)</a>', flags=re.DOTALL | re.IGNORECASE).findall(string=cat_block_cat[0])
        match_tags = re.compile(pattern='<a href="[^"]+">([^"]+)</a>', flags=re.DOTALL | re.IGNORECASE).findall(string=cat_block_tags[0])
        match_desc = re.compile(pattern='class="des-link">([^"]+)</em>', flags=re.DOTALL | re.IGNORECASE).findall(string=cat_block_desc[0])
        match_fav = re.compile(pattern='<li id="delete_fav_0" ><span><a href="' + site.url + 'my/favourites/videos/">Add to Favourites</a>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
        match_wlater = re.compile(pattern='<li id="delete_fav_1" ><span><a href="' + site.url + 'my/favourites/videos-watch-later/">Watch Later</a>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
        match_pl = re.compile(pattern='class="hidden"><a href="#add_to_playlist" data-video-id="\d+" data-fav-type="10" data-playlist-id="\d+">Add to \'([^"]+)\'</a>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
    except:
        return None
    str_models = ''
    str_tags = ''
    for url_md, model in match_model:
        model = model.strip()
        if get_subscription(url=url_md):
            model = '[COLOR blue]' + model + '[/COLOR]'
        if str_models == '':
            str_models = model
        else:
            str_models += ', ' + model
    for tag in match_tags:
        tag = tag.strip()
        if tag.startswith('-'):
            continue
        if str_tags == '':
            str_tags = tag
        else:
            str_tags += ', ' + tag
    str_info = '[COLOR deeppink]Description:[/COLOR] ' + utils.cleantext(', '.join(match_desc))
    str_info += '\n[COLOR deeppink]Member:[/COLOR] ' + member_name
    if match_model:
        str_info += '\n[COLOR deeppink]Models:[/COLOR] ' + str_models
    if match_pl:
        str_info += '\n[COLOR deeppink]Playlist[s]:[/COLOR] ' + ', '.join(match_pl)
    if match_fav:
        str_info += '\n[COLOR deeppink]Favourite[/COLOR]'
    if match_wlater:
        str_info += '\n[COLOR deeppink]Watch Later[/COLOR]'
    if match_cat:
        str_info += '\n[COLOR deeppink]Categories:[/COLOR] Porn, ' + ', '.join(match_cat)
    if match_tags:
        str_info += '\n[COLOR deeppink]Tags:[/COLOR] ' + str_tags
    str_info += '\n' + desc
    utils.textBox(heading='Video Info:', announce=str_info)


@site.register()
def PTGetInfoVideo(url):
    hdr = dict(utils.base_hdrs)
    hdr['Cookie'] = get_cookies()
    try:
        list_html = utils._getHtml(url=url, referer=site.url, headers=hdr)
    except:
        return None
    try:
        member_name = re.compile(pattern='<div class="username">\s+<a href="[^"]+">\s+([^"]+)\s+</a>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
        cat_block_model = re.compile(pattern='<span class="title-item">Models:</span>(.*?)<span class="title-item">Categories:</span>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
        cat_block_cat = re.compile(pattern='<span class="title-item">Categories:</span>(.*?)<span class="title-item">Tags:</span>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
        cat_block_tags = re.compile(pattern='<span class="title-item">Tags:</span>(.*?)<span class="title-item">Description:</span>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
        match_model = re.compile(pattern='<a href="([^"]+)"><i class="fa fa-star"></i> ([^"]+)</a>', flags=re.DOTALL | re.IGNORECASE).findall(string=cat_block_model[0])
        match_cat = re.compile(pattern='<a class="js-cat" href="[^"]+">([^"]+)</a>', flags=re.DOTALL | re.IGNORECASE).findall(string=cat_block_cat[0])
        match_tags = re.compile(pattern='<a href="[^"]+">([^"]+)</a>', flags=re.DOTALL | re.IGNORECASE).findall(string=cat_block_tags[0])
        match_fav = re.compile(pattern='<li id="delete_fav_0" ><span><a href="' + site.url + 'my/favourites/videos/">Add to Favourites</a>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
        match_wlater = re.compile(pattern='<li id="delete_fav_1" ><span><a href="' + site.url + 'my/favourites/videos-watch-later/">Watch Later</a>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
        match_pl = re.compile(pattern='class="hidden"><a href="#add_to_playlist" data-video-id="\d+" data-fav-type="10" data-playlist-id="\d+">Add to \'([^"]+)\'</a>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
    except:
        return None
    str_models = ''
    str_tags = ''
    for url_md, model in match_model:
        model = model.strip()
        if get_subscription(url=url_md):
            model = '[COLOR blue]' + model + '[/COLOR]'
        if str_models == '':
            str_models = model
        else:
            str_models += ', ' + model
    for tag in match_tags:
        tag = tag.strip()
        if tag.startswith('-'):
            continue
        if str_tags == '':
            str_tags = tag
        else:
            str_tags += ', ' + tag
    str_info = '[COLOR deeppink]Member:[/COLOR] ' + utils.cleantext(str(member_name[0]))
    if match_model:
        str_info += '\n[COLOR deeppink]Models:[/COLOR] ' + str_models
    if match_pl:
        str_info += '\n[COLOR deeppink]Playlist[s]:[/COLOR] ' + ', '.join(match_pl)
    if match_fav:
        str_info += '\n[COLOR deeppink]Favourite[/COLOR]'
    if match_wlater:
        str_info += '\n[COLOR deeppink]Watch Later[/COLOR]'
    if match_cat:
        str_info += '\n[COLOR deeppink]Categories:[/COLOR] Porn, ' + ', '.join(match_cat)
    if match_tags:
        str_info += '\n[COLOR deeppink]Tags:[/COLOR] ' + str_tags
    return str_info


@site.register()
def PTGetInfoPlaylist(name, url):
    hdr = dict(utils.base_hdrs)
    hdr['Cookie'] = get_cookies()
    try:
        list_html = utils._getHtml(url=url, referer=site.url, headers=hdr)
    except:
        return None
    _, member_name = get_member_url_check_name_url(url=url, list_html=list_html)
    if get_subscription(url=url, list_html=list_html):
        name = '[COLOR blue]' + name + '[/COLOR]'
    str_info = '[COLOR deeppink]Name:[/COLOR] ' + name
    cat_block = re.compile(pattern='<div id="tab_video_info"(.*?)<div id="tab_share"', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
    if cat_block:
        match_c = re.compile(pattern='<a href="[^"]+categories/[^"]+">([^"]+)</a>', flags=re.DOTALL | re.IGNORECASE).findall(string=cat_block[0])
        match_t = re.compile(pattern='<a href="[^"]+tags/[^"]+">([^"]+)</a>', flags=re.DOTALL | re.IGNORECASE).findall(string=cat_block[0])
        if match_c:
            str_info += '\n[COLOR deeppink]Categories:[/COLOR]' + ', '.join(match_c)
        if match_t:
            str_info += '\n[COLOR deeppink]Tags:[/COLOR]' + ', '.join(match_t)
    str_info += '\n[COLOR deeppink]Member:[/COLOR] ' + member_name
    utils.textBox(heading='Playlist Info:', announce=str_info)


@site.register()
def PTGetInfoModel(name, url):
    try:
        list_html = utils._getHtml(url=url, referer=site.url)
    except:
        return None
    blnSubscription = get_subscription(url=url, list_html=list_html)
    if blnSubscription:
        name = '[COLOR blue]' + name + '[/COLOR]'
    str_info = '[COLOR deeppink]Name:[/COLOR] ' + name
    description = re.compile(pattern='<div class="description-block">\s+<p>([^"]+)</p>\s+<div class="overlay"></div>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
    cat_block = re.compile(pattern='<div class="sidebar ">(.*?)<div class="info"><p>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
    if cat_block:
        match = re.compile(pattern='Total Videos:</span> (\d+)</p>.*?Followers:</span> (\d+)</p>.*?Video Views:</span> (\d+)</p>.*?Country:</span> ([^<]+)</p>.*?City:</span> ([^<]+)</p>.*?Age:</span> ([^<]+)</p>.*?Height:</span> ([^<]+)</p>.*?Weight:</span> ([^<]+)</p>', flags=re.DOTALL | re.IGNORECASE).findall(string=cat_block[0])
        for tot_videos, followers, vid_views, country, city, age, height, weight in match:
            str_info += '\n[COLOR deeppink]Total Videos: [/COLOR]' + tot_videos + ' ,[COLOR deeppink]Followers: [/COLOR]' + followers + '\n[COLOR deeppink]Video Views: [/COLOR]' + vid_views
            str_info += '\n[COLOR deeppink]Country: [/COLOR]' + country + ' ,[COLOR deeppink]City: [/COLOR]' + city
            str_info += '\n[COLOR deeppink]Age: [/COLOR]' + age + ' ,[COLOR deeppink]Height: [/COLOR]' + height + ' ,[COLOR deeppink]Weight: [/COLOR]' + weight
    str_info += '\n[COLOR deeppink]Description: [/COLOR]' + str(description[0])
    utils.textBox(heading='Model Info:', announce=str_info)


@site.register()
def PTGetInfoMember(url):
    hdr = dict(utils.base_hdrs)
    hdr['Cookie'] = get_cookies()
    url_info = ''
    name = ''
    str_info = ''
    if url.find('/my/') > 0 or url.find('/members/') > 0:
        url_root = url.split('?mode')[0]
        tmp_name_split = url_root.split('/')
        if url_root.find('/my/') > 0:
            url_info = '/'.join(tmp_name_split[:4]) + '/about/'
        elif url_root.find('/members/') > 0:
            url_info = '/'.join(tmp_name_split[:5]) + '/about/'
        try:
            content = utils._getHtml(url=url_info, referer=site.url, headers=hdr)
        except:
            return None
        cat_block = re.compile(pattern='<div class="info-blocks">(.*?)<div class="footer-margin">', flags=re.DOTALL | re.IGNORECASE).findall(string=content)
        cat_block_upl = re.compile(pattern='<span class="text"><b>Total uploaded videos:</b></span>(.*?)<div class="info-blocks">', flags=re.DOTALL | re.IGNORECASE).findall(string=content)
        str_member = re.compile(pattern='<div class="user-name">\s+<div class="value" style="display: flex;">([^"]+) </div>', flags=re.DOTALL | re.IGNORECASE).findall(string=content)
        subscribe = re.compile(pattern='<div class="user-buttons btn-subscribe-ajax">.*?<a href="([^"]+)" class="button subscribe "', flags=re.DOTALL | re.IGNORECASE).findall(string=content)
        if str_member:
            name = '[COLOR hotpink]' + str(str_member[0]) + '[/COLOR]'
        if subscribe:
            if str(subscribe[0]) == '#unsubscribe':
                name = '[COLOR blue]' + str(str_member[0]) + '[/COLOR]'
        match = re.compile(pattern='Last seen: <b>([^"]+)</b>.*?Rank: <b>(\d+)</b>.*?<b>([^"]+)</b> on Porntrex.com.*?<b>(\d+)</b> profile views.*?<b>(\d+)</b> video views.*?<b>(\d+)</b> subscribers', flags=re.DOTALL | re.IGNORECASE).findall(string=cat_block[0])
        match_upl = re.compile(pattern='<b>(\d+)</b> today.*?<b>(\d+)</b> yesterday.*?<b>(\d+)</b> this month.*?<b>(\d+)</b> last month.*?<b>(\d+)</b> this year', flags=re.DOTALL | re.IGNORECASE).findall(string=cat_block_upl[0])
        for lst_seen, rank, time, prf_views, vid_views, subscribers in match:
            str_info = '[COLOR deeppink]name: [/COLOR]' + name + '\n' + '[COLOR deeppink]Last seen: [/COLOR]' + lst_seen + '\n'
            str_info += '[COLOR deeppink]Rank: [/COLOR]' + rank + ', [COLOR deeppink]Time: [/COLOR]' + time + '\n' + '[COLOR deeppink]Profile views: [/COLOR]' + prf_views + '\n'
            str_info += '[COLOR deeppink]Video views: [/COLOR]' + vid_views + '\n' + '[COLOR deeppink]Subscribers: [/COLOR]' + subscribers + '\n'

        for uploaded_today, uploaded_yesterday, uploaded_month, uploaded_last_month, uploaded_year in match_upl:
            if int(uploaded_year[0]) > 0:
                str_info += '[COLOR deeppink]Uploaded: today: [/COLOR]' + uploaded_today + ', [COLOR deeppink]yesterday: [/COLOR]' + uploaded_yesterday + '\n'
                str_info += '[COLOR deeppink]this month: [/COLOR]' + uploaded_month + ', [COLOR deeppink]last month: [/COLOR]' + uploaded_last_month + '\n'
                str_info += '[COLOR deeppink]this year: [/COLOR]' + uploaded_year
    utils.textBox(heading='Video Info:', announce=str_info)


def set_fav_selector(url):
    hdr = dict(utils.base_hdrs)
    hdr['Cookie'] = get_cookies()
    m_color = 'hotpink'
    m_my = ''
    if '/members/' not in url:
        m_color = 'violet'
        m_my = 'my_'
    if url.find('?mode') > 0:
        url_root = url.split('?mode')[0]
    else:
        url_root = url
    try:
        list_html = utils._getHtml(url=url_root, referer=site.url, headers=hdr)
    except:
        return None
    match_sel = re.compile(pattern='<div class="user-info-section">(.*?)</ul>\s+<ul class="user-menu', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
    m_videos = re.compile(pattern='<a href="([^"]+)">\s+Videos\s+<e.*?>([^<]+)</em>', flags=re.DOTALL | re.IGNORECASE).findall(string=match_sel[0])
    m_videos_path = re.compile(pattern='<a href="([^"]+)">\s+Videos\s+</a>', flags=re.DOTALL | re.IGNORECASE).findall(string=match_sel[0])
    m_playlists = re.compile(pattern='<a href="([^"]+)">\s+Playlists\s+<e.*?>([^<]+)</em>', flags=re.DOTALL | re.IGNORECASE).findall(string=match_sel[0])
    m_playlists_path = re.compile(pattern='<a href="([^"]+)">\s+Playlists\s+</a>', flags=re.DOTALL | re.IGNORECASE).findall(string=match_sel[0])
    m_fav_videos = re.compile(pattern='<a href="([^"]+)">\s+Favourite Videos\s+<e.*?>([^<]+)</em>', flags=re.DOTALL | re.IGNORECASE).findall(string=match_sel[0])
    m_friends = re.compile(pattern='<a href="([^"]+)">\s+Friends\s+<e.*?>([^<]+)</em>', flags=re.DOTALL | re.IGNORECASE).findall(string=match_sel[0])
    int_w_later = re.compile(pattern='favourite_videos" data-parameters="[^"]+">Watch Later \((\d+)\)</a>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)

    for fav_url, count_fav in m_fav_videos:
        if count_fav == '99+':
            count_fav = get_number_videos(url=fav_url, section='fav_videos')
        if int(count_fav) > 0:
            url_fav = '{0}?mode=async&function=get_block&block_id=list_videos_{1}favourite_videos&fav_type=0&playlist_id=0&sort_by=&from_{1}fav_videos=1'.format(fav_url, m_my)
            name_fav = '[COLOR {0}]Favourite Videos ({1})[/COLOR]'.format(m_color, count_fav)
            if ptrange == 'No':
                site.add_dir2(name=name_fav, url=url_fav, page=1, mode='PTList', desc=set_trim_url(url=url_fav))
            else:
                site.add_dir2(name=name_fav, url=url_fav, page=1, mode='PTListSort', onelist=4, desc=set_trim_url(url=url_fav))

    if '/favourites/videos/' in url and 'fav_type=0' in url:
        if int_w_later:
            if url.find('/favourites/videos/') > 0 and int(int_w_later[0]) > 0:
                url_w_later = '{0}?mode=async&function=get_block&block_id=list_videos_{1}favourite_videos&fav_type=1&playlist_id=0&sort_by=&from_{1}fav_videos=1'.format(url_root, m_my)
                name_w_later = '[COLOR {0}]Watch Later ({1})[/COLOR]'.format(m_color, int_w_later[0])
                if ptrange == 'No':
                    site.add_dir2(name=name_w_later, url=url_w_later, page=1, mode='PTList', desc=set_trim_url(url=url_w_later))
                else:
                    site.add_dir2(name=name_w_later, url=url_w_later, page=1, mode='PTListSort', onelist=4, desc=set_trim_url(url=url_w_later))

        for fds_url, count in m_friends:
            if '/my/friends/' in fds_url:
                m_my = 'my_'
            url_friends = '{0}?mode=async&function=get_block&block_id=list_members_{1}friends&sort_by=added_date&from_friends=1'.format(fds_url, m_my)
            name_friends = '[COLOR {0}]Friends ({1})[/COLOR]'.format(m_color, count)
            if ptrange == 'No':
                site.add_dir2(name=name_friends, url=url_friends, page=1, mode='PTMembers', desc=set_trim_url(url=url_friends))
            else:
                site.add_dir2(name=name_friends, url=url_friends, page=1, mode='PTRangeList', onelist=4, section='PTMembers', desc=set_trim_url(url=url_friends))

        count_upl = 0
        upl_url = None
        for upl_url, count_upl in m_videos:
            if count_upl == '99+':
                count_upl = get_number_videos(url=upl_url, section='upl_videos')
        if not m_videos:
            if m_videos_path:
                upl_url = str(m_videos_path[0])
                count_upl = get_number_videos(url=upl_url, section='upl_videos')
        if int(count_upl) > 0 and upl_url:
            if '/my/videos/' in upl_url:
                m_my = 'my_'
            url_uploaded = '{0}?mode=async&function=get_block&block_id=list_videos_{1}uploaded_videos&sort_by=&from_{1}uploaded_videos=1'.format(upl_url, m_my)
            name_uploaded = '[COLOR {0}]Uploaded Videos ({1})[/COLOR]'.format(m_color, count_upl)
            if ptrange == 'No':
                site.add_dir2(name=name_uploaded, url=url_uploaded, page=1, mode='PTList', desc=set_trim_url(url=url_uploaded))
            else:
                site.add_dir2(name=name_uploaded, url=url_uploaded, page=1, mode='PTListSort', onelist=4, desc=set_trim_url(url=url_uploaded))

    if '/favourites/videos/' in url or '/videos/' in url:
        count_pl = 0
        pl_url = None
        for pl_url, count_pl in m_playlists:
            if count_pl == '99+':
                count_pl = get_number_playlists(m_my, list_html=list_html)
        if not m_playlists:
            if m_playlists_path:
                pl_url = str(m_playlists_path[0])
                count_pl = get_number_playlists(m_my, list_html=list_html)
        if int(count_pl) > 0 and pl_url:
            if '/my/playlists/' in pl_url:
                m_my = 'my_'
            url_playlists = '{0}?mode=async&function=get_block&block_id=list_playlists_{1}created_playlists&sort_by=last_content_date&from_{1}playlists=1'.format(pl_url, m_my)
            if ptrange == 'No':
                site.add_dir2(name='[COLOR {0}]Playlists ({1})[/COLOR]'.format(m_color, count_pl), url=url_playlists, page=1, mode='PTPlaylists', desc=set_trim_url(url=url_playlists))
            else:
                site.add_dir2(name='[COLOR {0}]Playlists ({1})[/COLOR]'.format(m_color, count_pl), url=url_playlists, page=1, mode='PTRangeList', onelist=4, section='PTPlaylists', desc=set_trim_url(url=url_playlists))


def get_member_url_check_name_url(url, list_html=None):
    hdr = dict(utils.base_hdrs)
    hdr['Cookie'] = get_cookies()
    if not list_html:
        try:
            list_html = utils._getHtml(url=url, referer=site.url, headers=hdr)
        except:
            return None
    match = re.compile(pattern='<div class="username">\s+<a href="([^"]+)">\s+([^"]+)\s+</a>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
    for member_url, name in match:
        name = utils.cleantext(name)
        list_html = utils._getHtml(url=member_url, referer=site.url, headers=hdr)
        blnSubscription = get_subscription(url=member_url, list_html=list_html)
        if blnSubscription:
            name = '[COLOR blue]' + name + '[/COLOR]'
        else:
            name = '[COLOR white]' + name + '[/COLOR]'
        match1 = re.compile(pattern='</style><script>var pageContext = {userId:([^"]+),loginUrl:', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
        if match1:
            return site.url + 'my/', name
        else:
            return str(member_url).strip(), name


def set_pages_to_match_onelist(url, page, onelist, list_html, section):
    global match
    hdr = dict(utils.base_hdrs)
    hdr['Cookie'] = get_cookies()
    if not list_html:
        try:
            list_html = utils._getHtml(url=url, referer=site.url, headers=hdr)
        except:
            return None
    if re.search(pattern='<li class="last"><a href="', string=list_html, flags=re.DOTALL | re.IGNORECASE):
        last_p = re.compile(pattern='<li class="last"><a href=".*?data-parameters.*?sort_by:[^"]+:(\d+)">', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)[0]
        last_p = int(last_p)
    else:
        last_p = 1
    if not onelist:
        range_page = last_p
    elif int(onelist)+page > last_p:
        range_page = last_p-page+1
    else:
        range_page = int(onelist)
    url = strip_end(text=url, suffix='=' + str(page)) + '=' + str(page+1)
    for page in range(page+1, range_page+page):
        try:
            list_html += utils._getHtml(url=url, referer=site.url, headers=hdr)
        except:
            return None
        url = strip_end(text=url, suffix='=' + str(page)) + '=' + str(page+1)
    if section == 'PTPlaylists':
        match = re.compile(pattern='<a href="([^"]+)" title="([^"]+)".*?data-original="([^"]+)".*?<div class="added"><em>([^"]+) ago</em></div>\s+<div class="rating positive">\s+([\d%]+)\s+</div>.*?<div class="viewsthumb">([^"]+) views</div>\s+<div class="totalplaylist">(\d+)', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
    elif section == 'PTSubscriptions':
        match = re.compile(pattern='<div class="item friend new">\s+<a href="([^"]+)" title="([^"]+)">.*?data-original="([^"]+)"', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
    elif section == 'PTList':
        match = re.compile(pattern='data-item-id=.*?href="([^"]+)".*?data-src="([^"]+)"(.*?)<div class="hd-text-icon(.*?)<div class="viewsthumb">([\d ]+) views</div>.*?clock-o"></i> ([^<]+)<.*?title="([^"]+)".*?<ul class="list-unstyled"><li>([^"]+)</li><li class="pull-right"><i class="fa fa-thumbs-o-up"></i> ([\d%]+)</li>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
    n_page = page + 1
    return match, n_page


def get_subscription(url, list_html=None):
    hdr = dict(utils.base_hdrs)
    hdr['Cookie'] = get_cookies()
    blnSubscription = False
    if not list_html:
        try:
            list_html = utils._getHtml(url=url, referer=site.url, headers=hdr)
        except:
            return None
        blnSubscription = False
    if '/videos/' in url or '/members/' in url:
        subscribe = re.compile(pattern='<div class="user-buttons btn-subscribe-ajax">\s+<a href="([^"]+)" class="button subscribe "', flags=re.DOTALL | re.IGNORECASE).findall(list_html)
    elif '/playlists/' in url:
        subscribe = re.compile(pattern='<div class="btn-subscribe">\s+<a href="([^"]+)" class="button"', flags=re.DOTALL | re.IGNORECASE).findall(list_html)
    else:
        subscribe = re.compile(pattern='<div class="btn-subscribe-ajax">\s+<a href="([^"]+)" class="button item subscribe "', flags=re.DOTALL | re.IGNORECASE).findall(list_html)
    if subscribe:
        if str(subscribe[0]) == '#unsubscribe':
            blnSubscription = True
    return blnSubscription


def page_list(url, page, mode, content, section=None):
    if not page:
        page = 1
    n_page = page + 1
    p_page = page - 1
    if re.search(pattern='<li class="last"><a href="', string=content, flags=re.DOTALL | re.IGNORECASE):
        last_p = re.compile(pattern='<li class="last"><a href=".*?data-parameters.*?sort_by:[^"]+:(\d+)">', flags=re.DOTALL | re.IGNORECASE).findall(string=content)[0]
        if page == int(last_p) or page > int(last_p):
            return None
        if re.search(pattern='<li class="next"><a href="', string=content, flags=re.DOTALL | re.IGNORECASE):
            next_p = re.compile(pattern='<li class="next"><a href="([^"]+)".*?data-block-id="([^"]+)" data-parameters="([^"]+):\d+">', flags=re.DOTALL | re.IGNORECASE).findall(string=content)[0]
            if url.find('?mode') > 0:
                url_next_page = url.replace('/{}/'.format(str(page)), '/{}/'.format(str(n_page)))
                url_next_page = strip_end(text=url_next_page, suffix='=' + str(page)) + '=' + str(n_page)
                if int(last_p) > page:
                    url_last_page = url.replace('/{}/'.format(str(page)), '/{}/'.format(str(last_p)))
                    url_last_page = strip_end(text=url_last_page, suffix='=' + str(page)) + '=' + str(last_p)
                    site.add_dir2(name='Last Page (' + str(last_p) + ')', url=url_last_page, mode=mode, iconimage=site.img_next, page=last_p, section=section, desc=set_trim_url(url=url_last_page))
                    if page > 1:
                        url_prev_page = url.replace('/{}/'.format(str(page)), '/{}/'.format(str(p_page)))
                        url_prev_page = strip_end(text=url_prev_page, suffix='=' + str(page)) + '=' + str(p_page)
                        site.add_dir2(name='Previous Page (' + str(p_page) + ')', url=url_prev_page, mode=mode, iconimage=site.img_next, page=p_page, section=section, desc=set_trim_url(url=url_prev_page))
                site.add_dir2(name='Next Page ('+str(n_page)+'/'+str(last_p)+')', url=url_next_page, mode=mode, iconimage=site.img_next, page=n_page, section=section, desc=set_trim_url(url=url_next_page))
            elif next_p[0][0] == '#':
                next_p2 = repair_url(text=clean_url(text=next_p[2]))
                url_next_page = url + '?mode=async&function=get_block&block_id=' + next_p[1] + '&' + next_p2 + '=' + str(n_page)
                if int(last_p) > page:
                    url_last_page = strip_end(text=url_next_page, suffix='=' + str(n_page)) + '=' + str(last_p)
                    site.add_dir2(name='Last Page (' + str(last_p) + ')', url=url_last_page, mode=mode, page=last_p, section=section, desc=set_trim_url(url=url_last_page))
                    if page > 1:
                        url_prev_page = strip_end(text=url_next_page, suffix='=' + str(n_page)) + '=' + str(p_page)
                        site.add_dir2(name='Previous Page (' + str(p_page) + ')', url=url_prev_page, mode=mode, page=p_page, section=section, desc=set_trim_url(url=url_prev_page))
                site.add_dir2(name='Next Page ('+str(n_page)+'/'+str(last_p)+')', url=url_next_page, mode=mode, page=n_page, section=section, desc=set_trim_url(url=url_next_page))
            else:
                next_p2 = repair_url(text=clean_url(text=next_p[2]))
                url_next_page = site.url[:-1] + next_p[0] + '?mode=async&function=get_block&block_id=' + next_p[1] + '&' + next_p2 + '=' + str(n_page)
                if int(last_p) > page:
                    url_last_page = url_next_page.replace('/{}/'.format(str(n_page)), '/{}/'.format(str(last_p)))
                    url_last_page = strip_end(text=url_last_page, suffix='=' + str(n_page)) + '=' + str(last_p)
                    site.add_dir2(name='Last Page (' + str(last_p) + ')', url=url_last_page, mode=mode, iconimage=site.img_next, page=last_p, section=section, desc=set_trim_url(url=url_last_page))
                    if page > 1:
                        url_prev_page = url_next_page.replace('/{}/'.format(str(n_page)), '/{}/'.format(str(p_page)))
                        url_prev_page = strip_end(text=url_prev_page, suffix='=' + str(n_page)) + '=' + str(p_page)
                        site.add_dir2(name='Previous Page (' + str(p_page) + ')', url=url_prev_page, mode=mode, iconimage=site.img_next, page=p_page, section=section, desc=set_trim_url(url=url_prev_page))
                site.add_dir2(name='Next Page ('+str(n_page)+'/'+str(last_p)+')', url=url_next_page, mode=mode, iconimage=site.img_next, page=n_page, section=section, desc=set_trim_url(url=url_next_page))
    else:
        if page > 1:
            url_prev_page = url.replace('/{}/'.format(str(page)), '/{}/'.format(str(p_page)))
            url_prev_page = strip_end(text=url_prev_page, suffix='=' + str(page)) + '=' + str(p_page)
            site.add_dir2(name='Previous Page (' + str(p_page) + ')', url=url_prev_page, mode=mode, iconimage=site.img_next, page=p_page, section=section, desc=set_trim_url(url=url_prev_page))


def page_list_search(url, page, content):
    n_page = page + 1
    p_page = page - 1
    if re.search(pattern='<li class="last"><a href="', string=content, flags=re.DOTALL | re.IGNORECASE):
        last_p = re.compile(pattern='<li class="last"><a href=".*?from:(\d+)">', flags=re.DOTALL | re.IGNORECASE).findall(string=content)[0]
        if page == int(last_p):
            return None
        if re.search(pattern='<li class="next"><a href="', string=content, flags=re.DOTALL | re.IGNORECASE):
            next_p = re.compile(pattern='<li class="next"><a href="([^"]+)".*?data-block-id="([^"]+)" data-parameters="([^"]+)category_ids:([^"]+):\d+">', flags=re.DOTALL | re.IGNORECASE).findall(string=content)[0]
            next_p2 = repair_url(text=clean_url(text=next_p[2]))
            if '/search/' in next_p[0]:
                next_p3 = repair_url(text=clean_url(text=next_p[3]))
                #resolve bug website: latest update relevance problem, change to relevance.
                if 'latest-updates' not in next_p[0] and 'post_date' in next_p3:
                    next_p3 = str(next_p3).replace('post_date', 'relevance')
                url_next_page = site.url[:-1] + next_p[0] + '?mode=async&function=get_block&block_id=' + next_p[1] + '&' + next_p2 + 'category_ids=' + next_p3 + '=' + str(n_page)
                if int(last_p) > page:
                    url_last_page = url_next_page.replace('/{}/'.format(str(n_page)), '/{}/'.format(str(last_p)))
                    url_last_page = strip_end(text=url_last_page, suffix='=' + str(n_page)) + '=' + str(last_p)
                    site.add_dir2(name='Last Page (' + str(last_p) + ')', url=url_last_page, mode='PTList', iconimage=site.img_next, page=last_p, desc=set_trim_url(url=url_last_page))
                    if page > 1:
                        url_prev_page = url_last_page.replace('/{}/'.format(str(last_p)), '/{}/'.format(str(p_page)))
                        url_prev_page = strip_end(text=url_prev_page, suffix='=' + str(last_p)) + '=' + str(p_page)
                        site.add_dir2(name='Previous Page (' + str(p_page) + ')', url=url_prev_page, mode='PTList', iconimage=site.img_next, page=p_page, desc=set_trim_url(url=url_prev_page))
                site.add_dir2(name='Next Page ('+str(n_page)+'/'+str(last_p)+')', url=url_next_page, mode='PTList', iconimage=site.img_next, page=n_page, desc=set_trim_url(url=url_next_page))
    else:
        if page > 1:
            url_prev_page = url.replace('/{}/'.format(str(page)), '/{}/'.format(str(p_page)))
            url_prev_page = strip_end(text=url_prev_page, suffix='=' + str(page)) + '=' + str(p_page)
            site.add_dir2(name='Previous Page (' + str(p_page) + ')', url=url_prev_page, mode='PTList', iconimage=site.img_next, page=p_page, desc=set_trim_url(url=url_prev_page))


def resolve_img(img):
    if img.startswith('//'):
        img = 'https:' + img
        img = str(img).replace(' ', '%20')
    return img


def resolve_hd(hd):
    if hd.find('4k') > 0:
        hd = '4k'
    elif hd.find('k4') > 0:
        hd = '4k'
    elif hd.find('2160p') > 0:
        hd = '4k'
    elif hd.find('1440p') > 0:
        hd = '1440p'
    elif hd.find('1080p') > 0:
        hd = '1080p'
    elif hd.find('720p') > 0:
        hd = '720p'
    elif hd.find('480p') > 0:
        hd = '480p'
    elif hd.find('360p') > 0:
        hd = '360p'
    elif hd.find('HD') > 0:
        hd = 'HD'
    else:
        hd = 'SD'
    return hd


def set_trim_url(url):
    url_ajax = None
    if debugurl:
        if url.find('?mode') > 0:
            url_ajax = url.split('?mode')[1]
            url = url.split('?mode')[0]
        tmp_name_split = url.split('/')
        tmp_name = '/'.join(tmp_name_split[:3])
        for x in range(3, len(tmp_name_split), 1):
            tmp_name = tmp_name + '/\n' + ''.join(tmp_name_split[x:x+1])
        if url_ajax and debugurl:
            tmp_name_split = url_ajax.split('&')
            tmp_name = tmp_name + '' + '?mode' + ''.join(tmp_name_split[:1])
            for x in range(1, len(tmp_name_split), 1):
                tmp_name = tmp_name + '&\n' + '&'.join(tmp_name_split[x:x+1])
        return tmp_name + '\n'
    else:
        return None


def strip_end(text, suffix):
    if suffix and text.endswith(suffix):
        return text[:-len(suffix)]
    return text


def set_strip_sort_url(url, int_split=3):
    url_ajax = None
    if url.find('?mode') > 0:
        url_ajax = url.split('?mode')[1]
        url = url.split('?mode')[0]
    tmp_name_split = url.split('/')
    sortUrl = '/'.join(tmp_name_split[int_split:])
    if url_ajax:
        sortBy = get_sort_by(url=url_ajax)
        sortUrl += ' [' + sortBy + ']'
    return sortUrl


def get_sort_by(url):
    if url.find('&sort_by=') > 0:
        match = re.compile(pattern='.*?&sort_by=([^"]+)&from[^"]+', flags=re.DOTALL | re.IGNORECASE).findall(string=url)
        for sortBy in match:
            return str(clean_url(text=sortBy))
    else:
        return ''


def get_next_folder_from_url(url, folder=None, int=1):
    tmp_name_split = url.split('/')
    next_folder = None
    for x in tmp_name_split:
        if x == folder:
            next_folder = tmp_name_split[tmp_name_split.index(x) - len(tmp_name_split) + int]
    return next_folder


def get_ajax_page1_url(url):
    hdr = dict(utils.base_hdrs)
    hdr['Cookie'] = get_cookies()
    try:
        list_html = utils._getHtml(url=url, referer=site.url, headers=hdr)
    except :
        return None
    if re.search(pattern='<li class="last"><a href="', string=list_html, flags=re.DOTALL | re.IGNORECASE):
        last_p = re.compile(pattern='<li class="last"><a href="([^"]+)".*?data-block-id="([^"]+)" data-parameters="([^"]+):\d">', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)[0]
        last_p2 = repair_url(text=clean_url(text=last_p[2]))
        page1 = ''
        if last_p[0][0] == '#':
            page1 = '1/'
        url += '{0}?mode=async&function=get_block&block_id=' + last_p[1] + '&' + last_p2 + '=1'.format(page1)
    return url


def get_ajax_search_page1_url(url, category=None):
    hdr = dict(utils.base_hdrs)
    hdr['Cookie'] = get_cookies()
    try:
        list_html = utils._getHtml(url=url, referer=site.url, headers=hdr)
    except:
        return None
    if re.search(pattern='<li class="last"><a href="', string=list_html, flags=re.DOTALL | re.IGNORECASE):
        if url.find('/search/') > 0:
            last_p = re.compile(pattern='<li class="last"><a href="([^"]+)".*?data-block-id="([^"]+)" data-parameters="([^"]+)category_ids:([^"]+)from:\d+">', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)[0]
            last_p2 = repair_url(text=clean_url(text=last_p[2]))
            last_p3 = repair_url(text=clean_url(text=last_p[3]))
            # resolve bug website: latest update relevance problem, change to relevance.
            if 'latest-updates' not in last_p[0] and 'post_date' in last_p3:
                last_p3 = last_p3.replace('post_date', 'relevance')
            if category:
                last_p3 = category + last_p3
            url += '?mode=async&function=get_block&block_id=' + last_p[1] + '&' + last_p2 + 'category_ids=' + last_p3 + 'from=1'
    return url


def clean_url(text):
    text = text.replace(':','=')
    text = text.replace(';','&')
    return text.strip()


#repair keyin asc
def repair_url(text):
    text = text.replace(' asc','')
    return text.strip()


def get_cookies():
    domain = site.url.split('www')[-1][:-1]
    cookiestr = 'kt_tcookie=1'
    for cookie in utils.cj:
        if cookie.domain == domain and cookie.name == 'PHPSESSID':
            cookiestr += '; PHPSESSID=' + cookie.value
        if cookie.domain == domain and cookie.name == 'kt_ips':
            cookiestr += '; kt_ips=' + cookie.value
        if cookie.domain == domain and cookie.name == 'kt_member':
            cookiestr += '; kt_member=' + cookie.value
    if ptlogged and 'kt_member' not in cookiestr:
        PTLogin(logged=False)
    return cookiestr


def get_section_from_url(url):
    section = None
    if '{0}members/'.format(site.url) in url:
        section = 'members'
        if '/friends/' in url:
            section = 'members_friends'
    elif '{0}playlists/'.format(site.url) in url:
        section = 'playlists'
    elif '{0}models/'.format(site.url) in url:
        section = 'models'
    elif '{0}categories/'.format(site.url) in url:
        section = 'categories'
    elif '{0}tags/'.format(site.url) in url:
        section = 'tags'
    elif '{0}my/friends/'.format(site.url) in url:
        section = 'friends'
    elif '{0}search/'.format(site.url) in url:
        section = 'search'
    return section


def get_mode_from_url(url):
    mode = None
    if 'list_videos' in url:
        mode = 'PTList'
    elif 'list_members_subscriptions_my_subscription' in url:
        mode = 'PTSubscriptions'
    return mode


def get_number_videos(url, section):
    count = 0
    hdr = dict(utils.base_hdrs)
    hdr['Cookie'] = get_cookies()
    try :
        list_html = utils._getHtml(url=url, referer=site.url, headers=hdr)
    except :
        return None
    try:
        if section == 'upl_videos':
            count = re.compile(pattern='uploaded_videos" data-parameters="">All Videos \((\d+)\)</a>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)[0]
        elif section == 'fav_videos':
            count = re.compile(pattern='<span class="icon type-fav"></span><strong>Favourites \((\d+)\)</strong>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)[0]
    except:
        return 0
    return count


#get number of playlist
def get_number_playlists(m_my, list_html):
    try:
        playlists_number = re.compile(pattern='data-block-id="list_videos_' + m_my + 'favourite_videos" data-parameters="playlist_id:(\d+)">[^"]+\(\d+\)</a>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
    except:
        return 0
    return len(playlists_number)




#write to ascci file
def PTWriteToFile(name, f_name):
    with open(f_name, "a") as x:
        x.write(name + '\n')


@site.register()
#Open Ascii File from profiledirectory, sections: tags, models
def OpenAsciiFile(url, sort, section):
    f_name = basics.profileDir + '/' + url
    with open(f_name, 'r') as f:
        f1 = f.readlines()
        if sort == 'sorted_name':
            sort_url = sorted(f1, key=lambda x: x.split(',')[0].lower())
        elif sort == 'default':
            sort_url = f1
        else:
            sort_url = f1
        for x in sort_url:
            name = x.strip()
            if section == 'tags':
                url_tags = x.replace(' ', '').strip()
                url_x = site.url + 'tags/' + url_tags + '/?mode=async&function=get_block&block_id=list_videos_common_videos_list_norm&sort_by=post_date&from4=1'
                site.add_dir2(name=name, url=url_x, page=1, mode='PTList', desc=set_trim_url(url=url_x))
            elif section == 'models':
                url_model = x.replace(' ', '-').strip()
                url_x = site.url + 'models/' + url_model + '/?mode=async&function=get_block&block_id=list_videos_common_videos_list_norm&sort_by=post_date&from4=1'
                site.add_dir2(name=name, url=url_x, page=1, mode='PTList', desc=set_trim_url(url=url_x))
    utils.eod()


@site.register()
#get modelnames from videopage url
def PTGetInfoModelName(url):
    hdr = dict(utils.base_hdrs)
    hdr['Cookie'] = get_cookies()
    try :
        list_html = utils._getHtml(url=url, referer=site.url, headers=hdr)
    except :
        return None
    try:
        cat_block_model = re.compile(pattern='<span class="title-item">Models:</span>(.*?)<span class="title-item">Categories:</span>', flags=re.DOTALL | re.IGNORECASE).findall(string=list_html)
        match_model = re.compile(pattern='<a href="([^"]+)"><i class="fa fa-star"></i> ([^"]+)</a>', flags=re.DOTALL | re.IGNORECASE).findall(string=cat_block_model[0])
    except:
        return None
    str_models = ''
    for url_md, model in match_model:
        model = model.strip()
        if str_models == '':
            str_models = model
        else:
            str_models += ', ' + model
    if match_model:
        return str_models
